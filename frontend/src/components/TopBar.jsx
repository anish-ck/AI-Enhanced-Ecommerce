import { Link, NavLink } from 'react-router-dom'

import { useAuth } from '../state/AuthContext'
import { useCart } from '../state/CartContext'

const navClass = ({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')

function TopBar() {
    const { user, logout } = useAuth()
    const { count } = useCart()

    return (
        <header className="topbar">
            <div className="brand">
                <Link to="/">SignalCart</Link>
                <span className="brand-tag">Phase 1</span>
            </div>
            <nav className="nav">
                <NavLink className={navClass} to="/">
                    Products
                </NavLink>
                <NavLink className={navClass} to="/cart">
                    Cart
                    <span className="badge">{count}</span>
                </NavLink>
                <NavLink className={navClass} to="/orders">
                    Orders
                </NavLink>
            </nav>
            <div className="auth">
                {user ? (
                    <>
                        <span className="user">{user.name}</span>
                        <button className="button ghost" type="button" onClick={logout}>
                            Log out
                        </button>
                    </>
                ) : (
                    <>
                        <NavLink className="button ghost" to="/login">
                            Log in
                        </NavLink>
                        <NavLink className="button primary" to="/signup">
                            Sign up
                        </NavLink>
                    </>
                )}
            </div>
        </header>
    )
}

export default TopBar
