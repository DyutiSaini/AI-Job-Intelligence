import { Link } from "react-router-dom";

function JobCard({ job }) {
  const score = Math.round(job.match_score);

  return (
    <div className="job-card">
      <div className="job-card-header">
        <div>
          <h3>{job.title}</h3>
          <p className="company-name">{job.company}</p>
        </div>

        <div className="match-score">
          <span>{score}%</span>
          <small>Match</small>
        </div>
      </div>

      <div className="job-section">
        <h4>Why it matches</h4>

        <p>
          {Array.isArray(job.why_it_matches)
            ? job.why_it_matches.join(" ")
            : job.why_it_matches ||
              "Good alignment with your profile."}
        </p>
      </div>

      <div className="skills-section">
        <div>
          <h4>Matched Skills</h4>

          <div className="skill-list">
            {job.matched_skills?.length > 0 ? (
              job.matched_skills.map((skill) => (
                <span
                  className="skill matched"
                  key={skill}
                >
                  {skill}
                </span>
              ))
            ) : (
              <span className="empty-skill">
                None
              </span>
            )}
          </div>
        </div>

        <div>
          <h4>Potential Gaps</h4>

          <div className="skill-list">
            {job.missing_skills?.length > 0 ? (
              job.missing_skills.map((skill) => (
                <span
                  className="skill missing"
                  key={skill}
                >
                  {skill}
                </span>
              ))
            ) : (
              <span className="empty-skill">
                None
              </span>
            )}
          </div>
        </div>
      </div>

      <div className="job-card-footer">
        <span>{job.source}</span>

        <Link
          to={`/job/${job.job_id}`}
          className="view-job-link"
        >
          View Job →
        </Link>
      </div>
    </div>
  );
}

export default JobCard;