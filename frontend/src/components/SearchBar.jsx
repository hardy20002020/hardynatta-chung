import PropTypes from "prop-types";

export default function SearchBar({
  search,
  onSearchChange,
  onSearch,
  onAdd,
  loading,
}) {

  function handleKeyDown(event) {

    if (event.key === "Enter") {

      onSearch();

    }

  }


  return (

    <div className="toolbar">

      <input
        type="text"
        placeholder="Search by name or email..."
        value={search}
        onChange={onSearchChange}
        onKeyDown={handleKeyDown}
        disabled={loading}
        className="search-input"
      />


      <button
        type="button"
        onClick={onSearch}
        disabled={loading}
        className="btn btn-primary"
      >
        Search
      </button>


      {onAdd && (

        <button
          type="button"
          onClick={onAdd}
          disabled={loading}
          className="btn btn-success"
        >
          + Add User
        </button>

      )}

    </div>

  );

}


SearchBar.propTypes = {

  search: PropTypes.string.isRequired,

  onSearchChange: PropTypes.func.isRequired,

  onSearch: PropTypes.func.isRequired,

  onAdd: PropTypes.func,

  loading: PropTypes.bool,

};


SearchBar.defaultProps = {

  onAdd: undefined,

  loading: false,

};