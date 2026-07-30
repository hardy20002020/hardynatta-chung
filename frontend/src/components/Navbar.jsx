import { useAuth } from "../auth/AuthContext";


export default function Navbar() {

  const { user, logout } = useAuth();


  return (
    <header>

      <h3>
        Welcome {user?.name}
      </h3>


      <button onClick={logout}>
        Logout
      </button>

    </header>
  );
}
