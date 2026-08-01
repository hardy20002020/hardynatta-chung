import { useEffect, useState } from "react";
import PropTypes from "prop-types";

export default function PermissionForm({
  initialData,
  loading,
  onSave,
  onCancel,
}) {
  const [name, setName] = useState("");

  useEffect(() => {
    setName(initialData?.name || "");
  }, [initialData]);

  function handleSubmit(event) {
    event.preventDefault();

    const trimmedName = name.trim();

    if (!trimmedName) {
      return;
    }

    onSave({
      name: trimmedName,
    });
  }

  return (
    <div className="card mb-3">
      <h2>
        {initialData
          ? "Edit Permission"
          : "Add Permission"}
      </h2>

      <form onSubmit={handleSubmit}>
        <div className="mb-2">
          <label htmlFor="permission-name">
            Permission Name
          </label>

          <input
            id="permission-name"
            type="text"
            value={name}
            onChange={(event) =>
              setName(event.target.value)
            }
            placeholder="Example: user.read"
            disabled={loading}
            autoFocus
          />
        </div>

        <div
          style={{
            display: "flex",
            gap: "10px",
          }}
        >
          <button
            type="submit"
            className="btn btn-success"
            disabled={loading || !name.trim()}
          >
            {loading ? "Saving..." : "Save"}
          </button>

          <button
            type="button"
            className="btn"
            onClick={onCancel}
            disabled={loading}
            style={{
              color: "#374151",
            }}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}

PermissionForm.propTypes = {
  initialData: PropTypes.shape({
    id: PropTypes.number,
    name: PropTypes.string,
  }),

  loading: PropTypes.bool,
  onSave: PropTypes.func.isRequired,
  onCancel: PropTypes.func.isRequired,
};

PermissionForm.defaultProps = {
  initialData: null,
  loading: false,
};
