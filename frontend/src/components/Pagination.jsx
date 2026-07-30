import PropTypes from "prop-types";

export default function Pagination({
  page,
  size,
  total,
  onPrevious,
  onNext,
}) {
  const totalPages = Math.max(1, Math.ceil(total / size));

  return (
    <div className="pagination">
      <button
        className="btn"
        onClick={onPrevious}
        disabled={page <= 1}
      >
        Previous
      </button>

      <span className="pagination-info">
        Page {page} of {totalPages}
      </span>

      <button
        className="btn"
        onClick={onNext}
        disabled={page >= totalPages}
      >
        Next
      </button>

      <span className="pagination-size">
        Size : {size}
      </span>

      <span className="pagination-total">
        Total : {total}
      </span>
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