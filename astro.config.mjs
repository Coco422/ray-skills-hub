import { defineConfig } from "astro/config";

const repoName = "ray-skills-hub";
const isActions = process.env.GITHUB_ACTIONS === "true";

export default defineConfig({
  site: process.env.SITE_URL ?? (isActions ? "https://coco422.github.io" : "http://localhost:4321"),
  base: process.env.SITE_BASE ?? (isActions ? `/${repoName}` : "/"),
  trailingSlash: "never",
});
