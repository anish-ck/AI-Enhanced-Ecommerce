import time
from itertools import count
from typing import Any

import httpx

from app import config


class MCPError(RuntimeError):
    pass


_RPC_ID = count(1)


def _ensure_config() -> tuple[str, str]:
    if not config.DATABRICKS_MCP_URL:
        raise MCPError("DATABRICKS_MCP_URL is not set")
    if not config.DATABRICKS_TOKEN:
        raise MCPError("DATABRICKS_TOKEN is not set")
    return config.DATABRICKS_MCP_URL.rstrip("/"), config.DATABRICKS_TOKEN


def _post(payload: dict[str, Any]) -> dict[str, Any]:
    url, token = _ensure_config()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        response = httpx.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        print("MCP ERROR:", str(exc))
        raise MCPError(str(exc)) from exc
    print("MCP STATUS:", response.status_code)
    print("MCP RAW RESPONSE:")
    print(response.text)
    try:
        response_json = response.json()
    except ValueError as exc:
        print("MCP ERROR:", str(exc))
        raise MCPError("MCP response was not valid JSON") from exc
    print("MCP JSON RESPONSE:")
    print(response_json)
    if isinstance(response_json, dict) and response_json.get("error"):
        error = response_json.get("error", {})
        message = error.get("message") if isinstance(error, dict) else str(error)
        raise MCPError(message or "MCP request returned an error")
    return response_json


def _extract_request_id(payload: Any) -> str | None:
    if isinstance(payload, dict):
        for key in ("request_id", "statement_id", "id"):
            value = payload.get(key)
            if value:
                return str(value)
        if "result" in payload:
            return _extract_request_id(payload["result"])
    return None


def _extract_statement_id(payload: Any) -> str | None:
    if isinstance(payload, dict):
        structured = payload.get("structuredContent")
        if isinstance(structured, dict) and structured.get("statement_id"):
            return str(structured.get("statement_id"))
        if payload.get("statement_id"):
            return str(payload.get("statement_id"))
        if "result" in payload:
            return _extract_statement_id(payload["result"])
    return None


def _extract_status(payload: Any) -> str | None:
    if isinstance(payload, dict):
        for key in ("status", "state"):
            value = payload.get(key)
            if value:
                return str(value).lower()
        if "result" in payload:
            return _extract_status(payload["result"])
    return None


def _normalize_columns(columns: Any) -> list[str]:
    if not columns:
        return []
    names: list[str] = []
    for idx, col in enumerate(columns):
        name = ""
        if isinstance(col, str):
            name = col
        elif isinstance(col, dict):
            name = col.get("name") or col.get("column_name") or col.get("field") or ""
        names.append(name or f"col_{idx}")
    return names


def _columns_from_manifest(manifest: Any) -> list[str]:
    if not isinstance(manifest, dict):
        return []
    schema = manifest.get("schema", {})
    if not isinstance(schema, dict):
        return []
    columns = schema.get("columns", [])
    if not isinstance(columns, list):
        return []
    return [col.get("name", "") for col in columns if isinstance(col, dict) and col.get("name")]


def _rows_from_matrix(rows: Any, columns: Any) -> list[dict]:
    if not rows:
        return []
    if isinstance(rows[0], dict):
        return rows
    col_names = _normalize_columns(columns)
    if not col_names and isinstance(rows[0], (list, tuple)):
        col_names = [f"col_{idx}" for idx in range(len(rows[0]))]
    return [dict(zip(col_names, row)) for row in rows]


def _parse_typed_value(value: Any) -> Any:
    if isinstance(value, dict):
        if "str" in value:
            return value.get("str")
        if "long" in value:
            return value.get("long")
        if "double" in value:
            return value.get("double")
        if "bool" in value:
            return value.get("bool")
    return None


def _rows_from_typed_array(rows: Any, columns: list[str]) -> list[dict]:
    if not rows:
        return []
    formatted_rows: list[dict] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        values = row.get("values", [])
        parsed_values = [_parse_typed_value(value) for value in values]
        formatted_rows.append(dict(zip(columns, parsed_values)))
    return formatted_rows


def _rows_from_content(content: Any) -> list[dict]:
    if not isinstance(content, list):
        return []
    for item in content:
        if not isinstance(item, dict):
            continue
        if "structuredContent" in item:
            rows = _extract_rows(item["structuredContent"])
            if rows:
                return rows
        if "data_array" in item:
            return _rows_from_matrix(item.get("data_array", []), item.get("columns"))
        if "rows" in item:
            return _rows_from_matrix(item.get("rows", []), item.get("columns"))
        if "data" in item:
            rows = _extract_rows(item["data"])
            if rows:
                return rows
    return []


def _extract_rows(payload: Any) -> list[dict]:
    if payload is None:
        return []
    if isinstance(payload, list):
        return _rows_from_matrix(payload, [])
    if isinstance(payload, dict):
        if "content" in payload:
            rows = _rows_from_content(payload.get("content"))
            if rows:
                return rows
        manifest_columns = _columns_from_manifest(payload.get("manifest", {}))
        result = payload.get("result")
        if isinstance(result, dict) and "structuredContent" in result:
            structured = result.get("structuredContent", {})
            structured_columns = _columns_from_manifest(structured.get("manifest", {}))
            typed_rows = (
                structured.get("result", {}).get("data_typed_array", [])
                if isinstance(structured, dict)
                else []
            )
            rows = _rows_from_typed_array(typed_rows, structured_columns)
            if rows:
                print("FORMATTED ROWS:")
                print(rows)
                return rows
        if isinstance(result, dict) and "content" in result:
            rows = _rows_from_content(result.get("content"))
            if rows:
                return rows
        if isinstance(result, dict) and "data_array" in result:
            return _rows_from_matrix(result.get("data_array", []), manifest_columns)
        if "data_array" in payload:
            return _rows_from_matrix(
                payload.get("data_array", []),
                manifest_columns or payload.get("columns") or payload.get("schema"),
            )
        if "structuredContent" in payload:
            return _extract_rows(payload["structuredContent"])
        if "data" in payload:
            return _extract_rows(payload["data"])
        if "rows" in payload:
            return _rows_from_matrix(payload["rows"], payload.get("columns") or payload.get("schema"))
        if "result" in payload:
            return _extract_rows(payload["result"])
    return []


def execute_sql(sql: str) -> list[dict]:
    payload = {
        "jsonrpc": "2.0",
        "id": next(_RPC_ID),
        "method": "tools/call",
        "params": {"name": "execute_sql", "arguments": {"query": sql}},
    }
    response = _post(payload)
    statement_id = _extract_statement_id(response)
    print("STATEMENT ID:", statement_id)
    if statement_id:
        return poll_sql_result(statement_id)
    request_id = _extract_request_id(response)
    if request_id:
        return poll_sql_result(request_id)
    raise MCPError("No statement_id returned from execute_sql")
    return _extract_rows(response)


def execute_sql_read_only(sql: str) -> list[dict]:
    payload = {
        "jsonrpc": "2.0",
        "id": next(_RPC_ID),
        "method": "tools/call",
        "params": {"name": "execute_sql_read_only", "arguments": {"query": sql}},
    }
    response = _post(payload)
    statement_id = _extract_statement_id(response)
    print("STATEMENT ID:", statement_id)
    if statement_id:
        return poll_sql_result(statement_id)
    request_id = _extract_request_id(response)
    if request_id:
        return poll_sql_result(request_id)
    raise MCPError("No statement_id returned from execute_sql")
    return _extract_rows(response)


def poll_sql_result(statement_id: str) -> list[dict]:
    for _ in range(10):
        payload = {
            "jsonrpc": "2.0",
            "id": next(_RPC_ID),
            "method": "tools/call",
            "params": {"name": "poll_sql_result", "arguments": {"statement_id": statement_id}},
        }
        response = _post(payload)
        structured_status = (
            response.get("result", {})
            .get("structuredContent", {})
            .get("status", {})
            .get("state")
            if isinstance(response, dict)
            else None
        )
        status = structured_status or _extract_status(response)
        print("QUERY STATUS:", status)
        if isinstance(status, str):
            status_upper = status.upper()
        else:
            status_upper = None
        if status_upper == "SUCCEEDED" or status in {"success", "succeeded", "finished", "done", "completed"}:
            return _extract_rows(response)
        if status_upper == "FAILED" or status in {"failed", "error"}:
            raise MCPError("MCP query failed")
        if status_upper in {"PENDING", "RUNNING", "QUEUED"} or status in {"pending", "running", "queued"}:
            time.sleep(1)
            continue
        time.sleep(0.5)
    raise MCPError("MCP query did not complete in time")
