import argparse
import csv
import os
import random


def sample_csv(
    input_path: str,
    output_path: str,
    key_field: str,
    target_rows: int,
    max_per_key: int,
    total_lines: int,
    oversample: float,
    seed: int,
    encoding: str,
) -> None:
    random.seed(seed)

    temp_path = f"{output_path}.tmp"
    key_counts = {}
    selected_rows = 0

    total_data_rows = max(total_lines, 1)
    sample_rate = min(1.0, (target_rows / total_data_rows) * oversample)

    with open(
        input_path, "r", newline="", encoding=encoding, errors="replace"
    ) as infile, open(temp_path, "w", newline="", encoding="utf-8") as outfile:
        reader = csv.DictReader(infile)
        if not reader.fieldnames:
            raise ValueError(f"No header found in {input_path}")

        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            key = (row.get(key_field) or "").strip()
            if not key:
                continue

            count = key_counts.get(key, 0)
            if count >= max_per_key:
                continue

            if random.random() <= sample_rate:
                writer.writerow(row)
                key_counts[key] = count + 1
                selected_rows += 1

    if selected_rows <= target_rows:
        os.replace(temp_path, output_path)
        print(f"Wrote {selected_rows} rows to {output_path}")
        return

    with open(temp_path, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    header, data_lines = lines[0], lines[1:]
    random.shuffle(data_lines)
    data_lines = data_lines[:target_rows]

    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.write(header)
        outfile.writelines(data_lines)

    os.remove(temp_path)
    print(f"Downsampled to {target_rows} rows at {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sample large CSV datasets")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--key-field", required=True)
    parser.add_argument("--target", type=int, required=True)
    parser.add_argument("--max-per-key", type=int, required=True)
    parser.add_argument("--total-lines", type=int, required=True)
    parser.add_argument("--oversample", type=float, default=2.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--encoding", default="utf-8")

    args = parser.parse_args()

    sample_csv(
        input_path=args.input,
        output_path=args.output,
        key_field=args.key_field,
        target_rows=args.target,
        max_per_key=args.max_per_key,
        total_lines=args.total_lines,
        oversample=args.oversample,
        seed=args.seed,
        encoding=args.encoding,
    )


if __name__ == "__main__":
    main()
