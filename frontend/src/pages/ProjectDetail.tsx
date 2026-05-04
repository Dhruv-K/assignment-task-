import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Layout from "../components/Layout";
import TaskBoard from "../components/TaskBoard";
import { getProject } from "../api/projects";

export default function ProjectDetail() {
  const { projectId } = useParams();
  const [project, setProject] = useState<any>(null);

  useEffect(() => {
    if (!projectId) return;
    const load = async () => {
      const data = await getProject(Number(projectId));
      setProject(data);
    };
    load();
  }, [projectId]);

  if (!project) {
    return (
      <Layout>
        <div className="max-w-5xl mx-auto">Loading...</div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-5xl mx-auto space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold">{project.name}</h1>
            {project.description && <div className="text-sm text-slate-600">{project.description}</div>}
          </div>
        </div>
        <TaskBoard projectId={Number(projectId)} />
      </div>
    </Layout>
  );
}
