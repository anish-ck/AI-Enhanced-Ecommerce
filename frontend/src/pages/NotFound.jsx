import { Link } from 'react-router-dom'

function NotFound() {
    return (
        <div className="page narrow">
            <div className="card">
                <h2>Page not found</h2>
                <p className="muted">The page you requested does not exist.</p>
                <Link className="button ghost" to="/">
                    Go home
                </Link>
            </div>
        </div>
    )
}

export default NotFound
