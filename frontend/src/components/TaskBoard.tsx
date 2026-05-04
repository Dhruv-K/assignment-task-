import { useEffect, useState } from "react";
import { Task, listProjectTasks, createTask, updateTask } from "../api/tasks";

type Props = {
  projectId: number;
};

export default function TaskBoard({ projectId }: Props) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");

  const load = async () => {
    const data = await listProjectTasks(projectId);
    setTasks(data);
  };

  useEffect(() => {
    load();
  }, [projectId]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    await createTask(projectId, { title });
    setTitle("");
    await load();
  };

  const moveTask = async (task: Task, status: Task["status"]) => {
    await updateTask(task.id, { status });
    await load();
  };

  const byStatus = (status: Task["status"]) => tasks.filter((t) => t.status === status);

  const column = (status: Task["status"], label: string) => (
    <div className="flex-1 bg-slate-100 rounded p-2">
      <div className="text-xs font-semibold mb-2">{label}</div>
      <div>
        {byStatus(status).map((t) => (
          <div key={t.id} className="bg-white rounded shadow p-2 mb-2 text-sm space-y-2">
            <div>{t.title}</div>
            <div className="flex gap-2 flex-wrap">
              {status !== "todo" && (
                <button className="text-xs px-2 py-1 rounded bg-slate-200" onClick={() => moveTask(t, "todo")}>Todo</button>
              )}
              {status !== "in_progress" && (
                <button className="text-xs px-2 py-1 rounded bg-amber-200" onClick={() => moveTask(t, "in_progress")}>In Progress</button>
              )}
              {status !== "done" && (
                <button className="text-xs px-2 py-1 rounded bg-emerald-200" onClick={() => moveTask(t, "done")}>Done</button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="space-y-4">
      <form onSubmit={handleCreate} className="flex gap-2">
        <input
          className="border rounded px-2 py-1 flex-1 text-sm"
          placeholder="New task title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <button className="bg-indigo-600 text-white text-sm px-3 py-1 rounded hover:bg-indigo-500">
          Add Task
        </button>
      </form>
      <div className="flex gap-3 flex-col md:flex-row">
        {column("todo", "Todo")}
        {column("in_progress", "In Progress")}
        {column("done", "Done")}
      </div>
    </div>
  );
}
