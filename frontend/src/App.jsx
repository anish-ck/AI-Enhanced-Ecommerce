import { BrowserRouter, Route, Routes } from 'react-router-dom'

import TopBar from './components/TopBar'
import Cart from './pages/Cart'
import Checkout from './pages/Checkout'
import Home from './pages/Home'
import Login from './pages/Login'
import NotFound from './pages/NotFound'
import Orders from './pages/Orders'
import AdminNewProduct from './pages/AdminNewProduct'
import ProductDetail from './pages/ProductDetail'
import Signup from './pages/Signup'
import { AuthProvider } from './state/AuthContext'
import { CartProvider } from './state/CartContext'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <CartProvider>
          <div className="app">
            <TopBar />
            <main className="main">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/products" element={<Home />} />
                <Route path="/products/:id" element={<ProductDetail />} />
                <Route path="/admin/products/new" element={<AdminNewProduct />} />
                <Route path="/cart" element={<Cart />} />
                <Route path="/checkout" element={<Checkout />} />
                <Route path="/orders" element={<Orders />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<Signup />} />
                <Route path="*" element={<NotFound />} />
              </Routes>
            </main>
            <footer className="footer">
              <div>
                <strong>SignalCart</strong>
                <p className="muted">
                  Phase 1 storefront. FastAPI + Postgres + React.
                </p>
              </div>
              <div className="footer-links">
                <span>Swagger</span>
                <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer">
                  API Docs
                </a>
              </div>
            </footer>
          </div>
        </CartProvider>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
