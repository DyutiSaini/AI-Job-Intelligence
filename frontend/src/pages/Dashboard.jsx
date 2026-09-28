import { useEffect, useState } from "react";
import { getJobMatches } from "../services/api";
import JobCard from "../components/JobCard";
import Navbar from "../components/Navbar";
import FilterBar from "../components/FilterBar";

function Dashboard() {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [filters, setFilters] = useState({
    location: "",
    company: "",
    skill: "",
    minScore: "0",
  });

  async function loadRecommendations(currentFilters = filters) {
    try {
      setLoading(true);
      setError("");

      const data = await getJobMatches({
        profileId: 2,
        limit: 10,
        minScore: Number(currentFilters.minScore),
        location: currentFilters.location,
        company: currentFilters.company,
        skill: currentFilters.skill,
      });

      setMatches(data.matches || []);
    } catch (err) {
      console.error(err);
      setError("Failed to load job recommendations.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadRecommendations();
  }, []);

  function handleApplyFilters() {
    loadRecommendations(filters);
  }

  function handleResetFilters() {
    const resetFilters = {
      location: "",
      company: "",
      skill: "",
      minScore: "0",
    };

    setFilters(resetFilters);
    loadRecommendations(resetFilters);
  }

  return (
    <div className="app-container">
      <Navbar />

      <main className="dashboard-container">
        <header className="dashboard-header">
          <h1>AI Job Intelligence</h1>

          <p>
            Personalized job recommendations based on your
            skills, profile and preferences.
          </p>
        </header>

        <FilterBar
          filters={filters}
          setFilters={setFilters}
          onApply={handleApplyFilters}
          onReset={handleResetFilters}
        />

        <section>
          <h2 className="section-title">
            Recommended Jobs
          </h2>

          {loading ? (
            <div className="loading">
              <h2>Finding matching jobs...</h2>
            </div>
          ) : error ? (
            <div className="error">
              <h2>{error}</h2>
            </div>
          ) : matches.length === 0 ? (
            <div className="empty-state">
              <p>
                No jobs match your current filters.
              </p>
            </div>
          ) : (
            <div className="jobs-grid">
              {matches.map((job) => (
                <JobCard
                  key={job.job_id}
                  job={job}
                />
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default Dashboard;