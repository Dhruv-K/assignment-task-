import api from "./client";

export type Task = {
  id: number;
  project_id: number;
  title: string;
  description: string | null;
  status: "todo" | "in_progress" | "done";
  priority: "low" | "medium" | "high";
  assignee_id: number | null;
  due_date: string | null;
};

export async function listProjectTasks(projectId: number, params?: Record<string, string | number | boolean>) {
  const res = await api.get(`/api/projects/${projectId}/tasks`, { params });
  return res.data as Task[];
}

export async function createTask(projectId: number, payload: Partial<Task>) {
  const res = await api.post(`/api/projects/${projectId}/tasks`, payload);
  return res.data as Task;
}

export async function updateTask(taskId: number, payload: Partial<Task>) {
  const res = await api.patch(`/api/tasks/${taskId}`, payload);
  return res.data as Task;
}
