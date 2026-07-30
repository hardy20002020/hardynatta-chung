import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";


export default function MainLayout({ children }) {

  return (
    <div>

      <Sidebar />

      <main>

        <Navbar />

        {children}

      </main>

    </div>
  );
}
