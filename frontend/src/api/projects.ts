import api from "./client";

export type Project = {
  id: number;
  name: string;
  description: string | null;
  owner_id: number;
  is_archived: boolean;
};

export async function listProjects(): Promise<Project[]> {
  const res = await api.get("/api/projects");
  return res.data;
}

export async function getProject(projectId: number) {
  const res = await api.get(`/api/projects/${projectId}`);
  return res.data;
}

export async function createProject(payload: { name: string; description?: string }) {
  const res = await api.post("/api/projects", payload);
  return res.data;
}
