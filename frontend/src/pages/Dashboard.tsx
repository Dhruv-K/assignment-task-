import Layout from "../components/Layout";
import ProjectList from "../components/ProjectList";

export default function Dashboard() {
  return (
    <Layout>
      <div className="max-w-5xl mx-auto space-y-6">
        <ProjectList />
      </div>
    </Layout>
  );
}
