import { useEffect, useState } from "react";

import {
  getUsers,
  getUser,
  createUser,
  updateUser,
  deleteUser,
} from "../api/userService";

import { useAuth } from "../auth/AuthContext";
import { hasPermission } from "../auth/permissionHelper";

import SearchBar from "../components/SearchBar";
import UserTable from "../components/UserTable";
import Pagination from "../components/Pagination";
import UserForm from "../components/UserForm";

import "../styles/user-management.css";


export default function UserManagement() {

  const { user } = useAuth();


  const canCreate =
    hasPermission(user, "user.create");

  const canEdit =
    hasPermission(user, "user.update");

  const canDelete =
    hasPermission(user, "user.delete");


  const [users, setUsers] =
    useState([]);


  const [meta, setMeta] = useState({
    page: 1,
    size: 10,
    total: 0,
  });


  const [page, setPage] =
    useState(1);

  const [size] =
    useState(10);

  const [search, setSearch] =
    useState("");


  const [loading, setLoading] =
    useState(true);

  const [saving, setSaving] =
    useState(false);

  const [error, setError] =
    useState("");


  const [showForm, setShowForm] =
    useState(false);

  const [selectedUser, setSelectedUser] =
    useState(null);



  useEffect(() => {

    document.title =
      "MAJE - User Management";

  }, []);



  useEffect(() => {

    loadUsers(page, search);

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page]);



  async function loadUsers(
    currentPage = page,
    currentSearch = search
  ) {

    try {

      setLoading(true);

      setError("");


      const response =
        await getUsers(
          currentPage,
          size,
          currentSearch
        );


      if (response.success) {

        setUsers(
          response.data.items
        );

        setMeta(
          response.data.meta
        );

      } else {

        setUsers([]);

        setMeta({
          page: currentPage,
          size,
          total: 0,
        });

        setError(
          response.message ||
          "Failed to load users."
        );

      }

    } catch (err) {

      console.error(err);


      setUsers([]);

      setMeta({
        page: currentPage,
        size,
        total: 0,
      });


      setError(
        "Failed to load users."
      );

    } finally {

      setLoading(false);

    }

  }



  async function handleSave(data) {

    const isCreate =
      !selectedUser;


    if (
      isCreate &&
      !canCreate
    ) {

      alert(
        "You do not have permission to create users."
      );

      return;

    }


    if (
      !isCreate &&
      !canEdit
    ) {

      alert(
        "You do not have permission to update users."
      );

      return;

    }


    setSaving(true);


    try {

      const response =
        isCreate
          ? await createUser(data)
          : await updateUser(
              selectedUser.id,
              data
            );


      if (response.success) {

        setShowForm(false);

        setSelectedUser(null);


        if (isCreate) {

          setSearch("");


          if (page !== 1) {

            setPage(1);

          } else {

            await loadUsers(
              1,
              ""
            );

          }

        } else {

          await loadUsers(
            page,
            search
          );

        }

      } else {

        alert(
          response.message ||
          "Failed to save user."
        );

      }

    } catch (err) {

      console.error(err);

      alert(
        "Failed to save user."
      );

    } finally {

      setSaving(false);

    }

  }



  async function handleEdit(
    selected
  ) {

    if (!canEdit) {

      alert(
        "You do not have permission to update users."
      );

      return;

    }


    try {

      const response =
        await getUser(
          selected.id
        );


      if (response.success) {

        setSelectedUser(
          response.data
        );

        setShowForm(true);

      } else {

        alert(
          response.message ||
          "Failed to load user."
        );

      }

    } catch (err) {

      console.error(err);

      alert(
        "Failed to load user."
      );

    }

  }



  async function handleDelete(
    selected
  ) {

    if (!canDelete) {

      alert(
        "You do not have permission to delete users."
      );

      return;

    }


    if (
      !window.confirm(
        `Hapus user "${selected.name}"?`
      )
    ) {

      return;

    }


    try {

      const response =
        await deleteUser(
          selected.id
        );


      if (response.success) {

        await loadUsers(
          page,
          search
        );

      } else {

        alert(
          response.message ||
          "Failed to delete user."
        );

      }

    } catch (err) {

      console.error(err);

      alert(
        "Failed to delete user."
      );

    }

  }



  async function handleSearch() {

    if (page !== 1) {

      setPage(1);

    } else {

      await loadUsers(
        1,
        search
      );

    }

  }



  function handleAdd() {

    if (!canCreate) {

      return;

    }


    setSelectedUser(null);

    setShowForm(true);

  }



  return (

    <div className="user-management">


      <h1 className="page-title">
        User Management
      </h1>


      <SearchBar
        search={search}
        onSearchChange={(e) =>
          setSearch(e.target.value)
        }
        onSearch={handleSearch}
        onAdd={
          canCreate
            ? handleAdd
            : undefined
        }
        loading={loading}
      />


      {showForm &&
        (
          (selectedUser && canEdit) ||
          (!selectedUser && canCreate)
        ) && (

          <UserForm
            initialData={
              selectedUser
            }
            loading={saving}
            onSave={handleSave}
            onCancel={() => {

              setShowForm(false);

              setSelectedUser(null);

            }}
          />

        )}


      {error && (

        <p className="error">
          {error}
        </p>

      )}


      <UserTable
        users={users}
        loading={loading}
        onEdit={handleEdit}
        onDelete={handleDelete}
        canEdit={canEdit}
        canDelete={canDelete}
      />


      <Pagination
        page={page}
        size={size}
        total={meta.total}
        onPrevious={() =>
          setPage((p) => p - 1)
        }
        onNext={() =>
          setPage((p) => p + 1)
        }
      />


    </div>

  );

}