function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">

        <div className="brand">
          <span className="brand-icon">AI</span>
          <span className="brand-name">
            Job Intelligence
          </span>
        </div>

        <div className="nav-links">
          <a href="/" className="nav-link active">
            Dashboard
          </a>

          <a href="/profile" className="nav-link">
            Profile
          </a>
        </div>

      </div>
    </nav>
  );
}

export default Navbar;