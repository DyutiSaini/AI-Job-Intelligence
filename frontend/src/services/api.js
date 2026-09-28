const API_BASE_URL = "http://127.0.0.1:8000";

export async function getJobs(params = {}) {
  const query = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (
      value !== undefined &&
      value !== null &&
      value !== ""
    ) {
      query.append(key, value);
    }
  });

  const url = `${API_BASE_URL}/jobs${
    query.toString() ? `?${query.toString()}` : ""
  }`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to fetch jobs");
  }

  return response.json();
}


export async function getJobMatches({
  profileId = 2,
  limit = 10,
  minScore = 0,
  location = "",
  company = "",
  skill = "",
} = {}) {
  const query = new URLSearchParams();

  query.append("profile_id", profileId);
  query.append("limit", limit);
  query.append("min_score", minScore);

  if (location) {
    query.append("location", location);
  }

  if (company) {
    query.append("company", company);
  }

  if (skill) {
    query.append("skill", skill);
  }

  const response = await fetch(
    `${API_BASE_URL}/jobs/matches?${query.toString()}`
  );

  if (!response.ok) {
    throw new Error(
      "Failed to fetch job recommendations"
    );
  }

  return response.json();
}


export async function getProfile(profileId = 2) {
  const response = await fetch(
    `${API_BASE_URL}/profile/${profileId}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch profile");
  }

  return response.json();
}


export async function getJob(jobId) {
  const response = await fetch(
    `${API_BASE_URL}/jobs/${jobId}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch job details");
  }

  return response.json();
}


export async function updateProfile(profileId, profile) {
  const response = await fetch(
    `${API_BASE_URL}/profile/${profileId}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(profile),
    }
  );

  if (!response.ok) {
    throw new Error("Failed to update profile");
  }

  return response.json();
}

export async function tailorResume({
  name,
  jobTitle,
  jobDescription,
  education = "",
  experience = "",
  candidateSkills = [],
}) {
  const response = await fetch(
    `${API_BASE_URL}/resume/tailor`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name,
        job_title: jobTitle,
        job_description: jobDescription,
        education,
        experience,
        candidate_skills: candidateSkills,
      }),
    }
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);

    throw new Error(
      errorData?.detail ||
        "Failed to tailor resume"
    );
  }

  return response.json();
}