import React from 'react';
import { Link } from 'react-router-dom';
function Navbar() {
  return (
    <div>
      <Link to="/">Home</Link>{" "}
      <Link to="/creds">Save Creds</Link>
    </div>
  );
};
export default Navbar;
