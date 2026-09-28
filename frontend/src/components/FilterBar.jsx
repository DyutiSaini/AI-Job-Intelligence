function FilterBar({ filters, setFilters, onApply, onReset }) {
  function handleChange(event) {
    const { name, value } = event.target;

    setFilters((current) => ({
      ...current,
      [name]: value,
    }));
  }

  return (
    <div className="filter-bar">
      <div className="filter-group">
        <label htmlFor="location">Location</label>

        <input
          id="location"
          name="location"
          type="text"
          placeholder="e.g. Bangalore"
          value={filters.location}
          onChange={handleChange}
        />
      </div>

      <div className="filter-group">
        <label htmlFor="company">Company</label>

        <input
          id="company"
          name="company"
          type="text"
          placeholder="e.g. Google"
          value={filters.company}
          onChange={handleChange}
        />
      </div>

      <div className="filter-group">
        <label htmlFor="skill">Skill</label>

        <input
          id="skill"
          name="skill"
          type="text"
          placeholder="e.g. Python"
          value={filters.skill}
          onChange={handleChange}
        />
      </div>

      <div className="filter-group">
        <label htmlFor="minScore">
          Minimum Match
        </label>

        <select
          id="minScore"
          name="minScore"
          value={filters.minScore}
          onChange={handleChange}
        >
          <option value="0">Any</option>
          <option value="30">30%+</option>
          <option value="50">50%+</option>
          <option value="60">60%+</option>
          <option value="70">70%+</option>
          <option value="80">80%+</option>
        </select>
      </div>

      <div className="filter-actions">
        <button
          type="button"
          className="apply-filter-btn"
          onClick={onApply}
        >
          Apply Filters
        </button>

        <button
          type="button"
          className="reset-filter-btn"
          onClick={onReset}
        >
          Reset
        </button>
      </div>
    </div>
  );
}

export default FilterBar;