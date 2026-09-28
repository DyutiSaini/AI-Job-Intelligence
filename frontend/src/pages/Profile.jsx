// import { useEffect, useState } from "react";
// import { getProfile, updateProfile } from "../services/api";

// function Profile() {
//   const [profile, setProfile] = useState({
//     roles: [],
//     locations: [],
//     skills: [],
//     graduation_year: "",
//     work_type: [],
//     companies: [],
//   });

//   const [loading, setLoading] = useState(true);
//   const [saving, setSaving] = useState(false);
//   const [message, setMessage] = useState("");
//   const [error, setError] = useState("");

//   useEffect(() => {
//     async function loadProfile() {
//       try {
//         const data = await getProfile(2);

//         setProfile({
//           roles: data.roles || [],
//           locations: data.locations || [],
//           skills: data.skills || [],
//           graduation_year: data.graduation_year || "",
//           work_type: data.work_type || [],
//           companies: data.companies || [],
//         });
//       } catch (err) {
//         console.error(err);
//         setError("Failed to load profile.");
//       } finally {
//         setLoading(false);
//       }
//     }

//     loadProfile();
//   }, []);

//   function handleTextChange(event) {
//     const { name, value } = event.target;

//     setProfile((current) => ({
//       ...current,
//       [name]: value,
//     }));
//   }

//   function handleListChange(event) {
//     const { name, value } = event.target;

//     setProfile((current) => ({
//       ...current,
//       [name]: value
//         .split(",")
//         .map((item) => item.trim())
//         .filter(Boolean),
//     }));
//   }

//   async function handleSave(event) {
//     event.preventDefault();

//     try {
//       setSaving(true);
//       setMessage("");
//       setError("");

//       const dataToSave = {
//         roles: profile.roles,
//         locations: profile.locations,
//         skills: profile.skills,
//         graduation_year: profile.graduation_year
//           ? Number(profile.graduation_year)
//           : null,
//         work_type: profile.work_type,
//         companies: profile.companies,
//       };

//       await updateProfile(2, dataToSave);

//       setMessage("Profile updated successfully.");
//     } catch (err) {
//       console.error(err);
//       setError("Failed to update profile.");
//     } finally {
//       setSaving(false);
//     }
//   }

//   if (loading) {
//     return (
//       <div className="loading">
//         <h2>Loading profile...</h2>
//       </div>
//     );
//   }

//   return (
//     <div className="app-container">
//       <main className="dashboard-container">

//         <div className="profile-header">
//           <h1>Your Profile</h1>

//           <p>
//             Update your preferences to improve AI job
//             recommendations.
//           </p>
//         </div>

//         <form
//           className="profile-form"
//           onSubmit={handleSave}
//         >

//           <div className="profile-field">
//             <label>Preferred Roles</label>

//             <input
//               type="text"
//               name="roles"
//               value={profile.roles.join(", ")}
//               onChange={handleListChange}
//               placeholder="Software Engineer Intern, Backend Intern"
//             />

//             <small>
//               Separate multiple roles with commas.
//             </small>
//           </div>

//           <div className="profile-field">
//             <label>Preferred Locations</label>

//             <input
//               type="text"
//               name="locations"
//               value={profile.locations.join(", ")}
//               onChange={handleListChange}
//               placeholder="Bangalore, Delhi NCR, Remote"
//             />

//             <small>
//               Separate multiple locations with commas.
//             </small>
//           </div>

//           <div className="profile-field">
//             <label>Skills</label>

//             <input
//               type="text"
//               name="skills"
//               value={profile.skills.join(", ")}
//               onChange={handleListChange}
//               placeholder="Python, FastAPI, PostgreSQL, Docker"
//             />

//             <small>
//               Separate skills with commas.
//             </small>
//           </div>

//           <div className="profile-field">
//             <label>Graduation Year</label>

//             <input
//               type="number"
//               name="graduation_year"
//               value={profile.graduation_year}
//               onChange={handleTextChange}
//               placeholder="2028"
//             />
//           </div>

//           <div className="profile-field">
//             <label>Work Type</label>

//             <input
//               type="text"
//               name="work_type"
//               value={profile.work_type.join(", ")}
//               onChange={handleListChange}
//               placeholder="Internship"
//             />
//           </div>

//           <div className="profile-field">
//             <label>Preferred Companies</label>

//             <input
//               type="text"
//               name="companies"
//               value={profile.companies.join(", ")}
//               onChange={handleListChange}
//               placeholder="Google, Microsoft, Amazon, NVIDIA"
//             />
//           </div>

//           {message && (
//             <div className="success-message">
//               {message}
//             </div>
//           )}

//           {error && (
//             <div className="error-message">
//               {error}
//             </div>
//           )}

//           <button
//             type="submit"
//             className="save-profile-btn"
//             disabled={saving}
//           >
//             {saving ? "Saving..." : "Save Profile"}
//           </button>

//         </form>
//       </main>
//     </div>
//   );
// }

// export default Profile;

import { useEffect, useState } from "react";
import { getProfile, updateProfile } from "../services/api";

function Profile() {
  const [profile, setProfile] = useState({
    name: "",
    education: "",
    experience: "",
    roles: [],
    locations: [],
    skills: [],
    graduation_year: "",
    work_type: [],
    companies: [],
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadProfile() {
      try {
        const data = await getProfile(2);

        setProfile({
          name: data.name || "",
          education: data.education || "",
          experience: data.experience || "",
          roles: data.roles || [],
          locations: data.locations || [],
          skills: data.skills || [],
          graduation_year: data.graduation_year || "",
          work_type: data.work_type || [],
          companies: data.companies || [],
        });
      } catch (err) {
        console.error(err);
        setError("Failed to load profile.");
      } finally {
        setLoading(false);
      }
    }

    loadProfile();
  }, []);

  function handleTextChange(event) {
    const { name, value } = event.target;

    setProfile((current) => ({
      ...current,
      [name]: value,
    }));
  }

  function handleListChange(event) {
    const { name, value } = event.target;

    setProfile((current) => ({
      ...current,
      [name]: value
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean),
    }));
  }

  async function handleSave(event) {
    event.preventDefault();

    try {
      setSaving(true);
      setMessage("");
      setError("");

      const dataToSave = {
        name: profile.name,
        education: profile.education,
        experience: profile.experience,

        roles: profile.roles,
        locations: profile.locations,
        skills: profile.skills,

        graduation_year: profile.graduation_year
          ? Number(profile.graduation_year)
          : null,

        work_type: profile.work_type,
        companies: profile.companies,
      };

      await updateProfile(2, dataToSave);

      setMessage("Profile updated successfully.");
    } catch (err) {
      console.error(err);
      setError("Failed to update profile.");
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <h2>Loading profile...</h2>
      </div>
    );
  }

  return (
    <div className="app-container">
      <main className="dashboard-container">

        <div className="profile-header">
          <h1>Your Profile</h1>

          <p>
            Update your personal information and preferences
            to improve AI job recommendations and resume tailoring.
          </p>
        </div>

        <form
          className="profile-form"
          onSubmit={handleSave}
        >

          {/* =========================
              PERSONAL INFORMATION
          ========================== */}

          <div className="profile-field">
            <label>Full Name</label>

            <input
              type="text"
              name="name"
              value={profile.name}
              onChange={handleTextChange}
              placeholder="Your full name"
            />

            <small>
              Used for personalized resume tailoring.
            </small>
          </div>

          <div className="profile-field">
            <label>Education</label>

            <textarea
              name="education"
              value={profile.education}
              onChange={handleTextChange}
              placeholder="B.Tech in Computer Science Engineering, IGDTUW, 2024-2028"
              rows="3"
            />

            <small>
              Add your degree, university and relevant education details.
            </small>
          </div>

          <div className="profile-field">
            <label>Experience</label>

            <textarea
              name="experience"
              value={profile.experience}
              onChange={handleTextChange}
              placeholder="Software Engineering Intern at XYZ. Worked on backend APIs using Python and FastAPI."
              rows="5"
            />

            <small>
              Add internships, research experience, work experience,
              or other relevant professional experience.
            </small>
          </div>

          {/* =========================
              JOB PREFERENCES
          ========================== */}

          <div className="profile-field">
            <label>Preferred Roles</label>

            <input
              type="text"
              name="roles"
              value={profile.roles.join(", ")}
              onChange={handleListChange}
              placeholder="Software Engineer Intern, Backend Intern"
            />

            <small>
              Separate multiple roles with commas.
            </small>
          </div>

          <div className="profile-field">
            <label>Preferred Locations</label>

            <input
              type="text"
              name="locations"
              value={profile.locations.join(", ")}
              onChange={handleListChange}
              placeholder="Bangalore, Delhi NCR, Remote"
            />

            <small>
              Separate multiple locations with commas.
            </small>
          </div>

          <div className="profile-field">
            <label>Skills</label>

            <input
              type="text"
              name="skills"
              value={profile.skills.join(", ")}
              onChange={handleListChange}
              placeholder="Python, FastAPI, PostgreSQL, Docker"
            />

            <small>
              Separate skills with commas.
            </small>
          </div>

          <div className="profile-field">
            <label>Graduation Year</label>

            <input
              type="number"
              name="graduation_year"
              value={profile.graduation_year}
              onChange={handleTextChange}
              placeholder="2028"
            />
          </div>

          <div className="profile-field">
            <label>Work Type</label>

            <input
              type="text"
              name="work_type"
              value={profile.work_type.join(", ")}
              onChange={handleListChange}
              placeholder="Internship"
            />
          </div>

          <div className="profile-field">
            <label>Preferred Companies</label>

            <input
              type="text"
              name="companies"
              value={profile.companies.join(", ")}
              onChange={handleListChange}
              placeholder="Google, Microsoft, Amazon, NVIDIA"
            />
          </div>

          {/* =========================
              STATUS
          ========================== */}

          {message && (
            <div className="success-message">
              {message}
            </div>
          )}

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <button
            type="submit"
            className="save-profile-btn"
            disabled={saving}
          >
            {saving ? "Saving..." : "Save Profile"}
          </button>

        </form>
      </main>
    </div>
  );
}

export default Profile;