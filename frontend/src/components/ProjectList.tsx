import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { createProject, listProjects, Project } from "../api/projects";

export default function ProjectList() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const navigate = useNavigate();

  const load = async () => {
    const data = await listProjects();
    setProjects(data);
  };

  useEffect(() => {
    load();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;
    await createProject({ name, description });
    setName("");
    setDescription("");
    await load();
  };

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold mb-2">Projects</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {projects.map((p) => (
          <button
            key={p.id}
            className="bg-white rounded shadow p-3 text-left hover:ring-2 hover:ring-indigo-500"
            onClick={() => navigate(`/projects/${p.id}`)}
          >
            <div className="font-medium">{p.name}</div>
            <div className="text-xs text-slate-500 line-clamp-2">{p.description}</div>
          </button>
        ))}
      </div>
      <form onSubmit={handleCreate} className="bg-white rounded shadow p-4 space-y-2 max-w-md">
        <div className="font-semibold text-sm">Create Project</div>
        <input
          className="border rounded px-2 py-1 w-full text-sm"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <textarea
          className="border rounded px-2 py-1 w-full text-sm"
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <button className="bg-indigo-600 text-white text-sm px-3 py-1 rounded hover:bg-indigo-500">
          Create
        </button>
      </form>
    </div>
  );
}
