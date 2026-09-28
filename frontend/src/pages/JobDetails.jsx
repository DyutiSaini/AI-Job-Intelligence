import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import {
  getJob,
  getJobMatches,
  getProfile,
  tailorResume,
} from "../services/api";
function JobDetails() {
  const { jobId } = useParams();

  const [job, setJob] = useState(null);
  const [match, setMatch] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [tailoring, setTailoring] = useState(false);
  const [tailorError, setTailorError] = useState("");
  const [tailorResult, setTailorResult] = useState(null);
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    async function loadJobDetails() {
      try {
        setLoading(true);
        setError("");

        const jobData = await getJob(jobId);

        const matchData = await getJobMatches({
          profileId: 2,
          limit: 50,
        });

        const profileData = await getProfile(2);

        const matchedJob = matchData.matches?.find(
          (item) => item.job_id === Number(jobId)
        );

        setJob(jobData);
        setMatch(matchedJob || null);
        setProfile(profileData);
      } catch (err) {
        console.error(err);
        setError("Failed to load job details.");
      } finally {
        setLoading(false);
      }
    }

    loadJobDetails();
  }, [jobId]);

async function handleTailorResume() {
    try {
      setTailoring(true);
      setTailorError("");
      setTailorResult(null);

      const currentProfile = await getProfile(2);

      console.log(
        "Profile used for tailoring:",
        currentProfile
      );

      const result = await tailorResume({
        name: currentProfile?.name || "",
        jobTitle: job.title,
        jobDescription: job.description,
        education: currentProfile?.education || "",
        experience: currentProfile?.experience || "",
        candidateSkills: currentProfile?.skills || [],
      });

      setTailorResult(result);
    } catch (err) {
      console.error(err);

      setTailorError(
        err.message || "Failed to tailor resume."
      );
    } finally {
      setTailoring(false);
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <h2>Loading job details...</h2>
      </div>
    );
  }

  if (error || !job) {
    return (
      <div className="error">
        <h2>{error || "Job not found."}</h2>
        <Link to="/">← Back to Dashboard</Link>
      </div>
    );
  }

  return (
    <div className="app-container">
      <main className="dashboard-container">
        <Link to="/" className="back-link">
          ← Back to Dashboard
        </Link>

        <div className="job-details-card">
          <div className="job-details-header">
            <div>
              <h1>{job.title}</h1>
              <p className="company-name">
                {job.company}
              </p>
            </div>

            {match && (
              <div className="match-score large">
                <span>{Math.round(match.match_score)}%</span>
                <small>Match</small>
              </div>
            )}
          </div>

          <div className="job-meta">
            <span>
              📍 {job.locations?.join(", ") || "Location not specified"}
            </span>

            <span>
              🏢 {job.source}
            </span>

            {job.employment_type && (
              <span>
                💼 {job.employment_type}
              </span>
            )}
          </div>

          {match && (
            <section className="details-section">
              <h2>AI Match Analysis</h2>

              <div className="score-grid">
                <div>
                  <strong>{Math.round(match.match_score)}%</strong>
                  <span>Overall Match</span>
                </div>

                <div>
                  <strong>{Math.round(match.skill_score)}%</strong>
                  <span>Skill Match</span>
                </div>

                <div>
                  <strong>
                    {Math.round(match.semantic_score)}%
                  </strong>
                  <span>Semantic Match</span>
                </div>

                <div>
                  <strong>
                    {Math.round(match.location_score)}%
                  </strong>
                  <span>Location Match</span>
                </div>
              </div>
            </section>
          )}

          {match && (
            <section className="details-section">
              <h2>Why This Job Matches</h2>

              <p>
                {Array.isArray(match.why_it_matches)
                  ? match.why_it_matches.join(" ")
                  : match.why_it_matches ||
                    "This job has some alignment with your profile."}
              </p>
            </section>
          )}

          {match && (
            <section className="details-section">
              <div className="details-skill-columns">
                <div>
                  <h2>Matched Skills</h2>

                  <div className="skill-list">
                    {match.matched_skills?.length > 0 ? (
                      match.matched_skills.map((skill) => (
                        <span
                          className="skill matched"
                          key={skill}
                        >
                          {skill}
                        </span>
                      ))
                    ) : (
                      <span className="empty-skill">
                        No direct skill matches
                      </span>
                    )}
                  </div>
                </div>

                <div>
                  <h2>Potential Gaps</h2>

                  <div className="skill-list">
                    {match.missing_skills?.length > 0 ? (
                      match.missing_skills.map((skill) => (
                        <span
                          className="skill missing"
                          key={skill}
                        >
                          {skill}
                        </span>
                      ))
                    ) : (
                      <span className="empty-skill">
                        No major skill gaps
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </section>
          )}

          <section className="details-section">
              <h2>Job Description</h2>

              <p className="job-description">
                {job.description}
              </p>
            </section>


            {/* =====================================================
                AI RESUME TAILORING
            ===================================================== */}

            <section className="details-section resume-tailor-section">
              <h2>AI Resume Tailoring</h2>

              <p>
                Tailor your resume for this job using your profile
                and the job requirements.
              </p>

              <button
                type="button"
                className="apply-button"
                onClick={handleTailorResume}
                disabled={tailoring}
              >
                {tailoring
                  ? "Tailoring Resume..."
                  : "✨ Tailor My Resume"}
              </button>

              {tailorError && (
                <p className="error-message">
                  {tailorError}
                </p>
              )}

              {tailorResult && (
                <div className="tailor-result">

                  <div className="ats-score-box">
                    <strong>
                      {Math.round(
                        tailorResult.ats_analysis.ats_score
                      )}%
                    </strong>

                    <span>ATS Match</span>
                  </div>

                  <div>
                    <h3>Matched Required Skills</h3>

                    <div className="skill-list">
                      {tailorResult.ats_analysis.required_matches
                        ?.length > 0 ? (
                        tailorResult.ats_analysis.required_matches.map(
                          (skill) => (
                            <span
                              className="skill matched"
                              key={skill}
                            >
                              {skill}
                            </span>
                          )
                        )
                      ) : (
                        <span className="empty-skill">
                          No required skills matched
                        </span>
                      )}
                    </div>
                  </div>

                  <div>
                    <h3>Skill Gaps</h3>

                    <div className="skill-list">
                      {tailorResult.ats_analysis.required_gaps
                        ?.length > 0 ? (
                        tailorResult.ats_analysis.required_gaps.map(
                          (skill) => (
                            <span
                              className="skill missing"
                              key={skill}
                            >
                              {skill}
                            </span>
                          )
                        )
                      ) : (
                        <span className="empty-skill">
                          No required skill gaps
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="tailor-content">
                    <h3>Tailored Professional Summary</h3>

                    <p>
                      {tailorResult.tailored_summary}
                    </p>
                  </div>

                  <div className="tailor-content">
                    <h3>Tailored Experience</h3>

                    <p>
                      {tailorResult.tailored_experience}
                    </p>
                  </div>

                  {tailorResult.tailoring_notes?.length > 0 && (
                    <div className="tailor-content">
                      <h3>Tailoring Notes</h3>

                      <ul>
                        {tailorResult.tailoring_notes.map(
                          (note, index) => (
                            <li key={index}>{note}</li>
                          )
                        )}
                      </ul>
                    </div>
                  )}

                </div>
              )}
            </section>


            <div className="job-details-footer">
              <a
                href={job.url}
                target="_blank"
                rel="noopener noreferrer"
                className="apply-button"
              >
                View Original Job →
              </a>
            </div>
        </div>
      </main>
    </div>
  );
}

export default JobDetails;


