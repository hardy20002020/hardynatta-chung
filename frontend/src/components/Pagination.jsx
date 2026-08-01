import PropTypes from "prop-types";

export default function Pagination({
  page,
  size,
  total,
  onPrevious,
  onNext,
}) {
  const totalPages = Math.max(
    1,
    Math.ceil(total / size)
  );

  return (
    <div className="pagination">

      <button
        className="btn btn-primary"
        onClick={onPrevious}
        disabled={page <= 1}
      >
        ← Previous
      </button>

      <div className="pagination-info">
        <strong>
          Page {page}
        </strong>{" "}
        of {totalPages}
      </div>

      <button
        className="btn btn-primary"
        onClick={onNext}
        disabled={page >= totalPages}
      >
        Next →
      </button>

      <div className="pagination-meta">
        <span>
          Size: <strong>{size}</strong>
        </span>

        <span>
          Total: <strong>{total}</strong>
        </span>
      </div>

    </div>
  );
}

Pagination.propTypes = {
  page: PropTypes.number.isRequired,
  size: PropTypes.number.isRequired,
  total: PropTypes.number.isRequired,
  onPrevious: PropTypes.func.isRequired,
  onNext: PropTypes.func.isRequired,
};