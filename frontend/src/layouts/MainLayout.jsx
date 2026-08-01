import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

export default function MainLayout({ children }) {
  return (
    <div className="layout">
      <Sidebar />

      <div className="content">
        <Navbar />

        <main className="page-content">
          {children}
        </main>
      </div>
    </div>
  );
}