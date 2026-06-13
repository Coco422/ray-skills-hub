import { readFileSync } from "node:fs";
import { join } from "node:path";

import matter from "gray-matter";
import YAML from "yaml";

const ROOT = process.cwd();
const REPO = "Coco422/ray-skills-hub";
const BRANCH = "main";

type Catalog = {
  hub?: {
    name?: string;
    version?: string;
    updated?: string;
  };
  skills?: CatalogSkill[];
};

export type CatalogSkill = {
  id: string;
  path: string;
  source: "team" | "personal" | string;
  owner?: string;
  recommended?: boolean;
  maturity?: "stable" | "beta" | "experimental" | string;
  version?: string;
  license?: string;
  upstream?: null | {
    repo?: string;
    ref?: string;
  };
  tags?: string[];
  last_reviewed?: string;
};

export type Skill = CatalogSkill & {
  name: string;
  description: string;
  body: string;
  summary: string;
  rawMdUrl: string;
  githubUrl: string;
  githubMdUrl: string;
  installCommand: string;
};

export type HubMeta = {
  name: string;
  version: string;
  updated: string;
};

function readCatalog(): Catalog {
  const raw = readFileSync(join(ROOT, "CATALOG.yaml"), "utf-8");
  const catalog = YAML.parse(raw);
  if (!catalog || !Array.isArray(catalog.skills)) {
    throw new Error("CATALOG.yaml must contain a skills list.");
  }
  return catalog;
}

function readSkillMarkdown(skillPath: string) {
  const raw = readFileSync(join(ROOT, skillPath, "SKILL.md"), "utf-8");
  return matter(raw);
}

function normalizeDescription(value: unknown): string {
  if (typeof value !== "string") return "";
  return value.replace(/\s+/g, " ").trim();
}

function extractSummary(markdown: string): string {
  const withoutCode = markdown.replace(/```[\s\S]*?```/g, " ");
  const lines = withoutCode
    .split("\n")
    .map((line) => line.replace(/^#+\s*/, "").trim())
    .filter((line) => line && !line.startsWith(">") && !line.startsWith("- "));
  return (lines[0] ?? "").replace(/\*\*/g, "").slice(0, 180);
}

function sortSkills(a: Skill, b: Skill): number {
  const sourceRank = Number(a.source !== "team") - Number(b.source !== "team");
  if (sourceRank) return sourceRank;

  const maturityOrder = new Map([
    ["stable", 0],
    ["beta", 1],
    ["experimental", 2],
  ]);
  const maturityRank =
    (maturityOrder.get(a.maturity ?? "") ?? 9) - (maturityOrder.get(b.maturity ?? "") ?? 9);
  if (maturityRank) return maturityRank;

  return a.id.localeCompare(b.id);
}

export function getHubMeta(): HubMeta {
  const catalog = readCatalog();
  return {
    name: catalog.hub?.name ?? "ray-skills-hub",
    version: catalog.hub?.version ?? "unknown",
    updated: catalog.hub?.updated ?? "unknown",
  };
}

export function getSkills(): Skill[] {
  const catalog = readCatalog();
  return (catalog.skills ?? [])
    .map((entry) => {
      const parsed = readSkillMarkdown(entry.path);
      const name = typeof parsed.data.name === "string" ? parsed.data.name : entry.id;
      const description = normalizeDescription(parsed.data.description);
      const rawMdUrl = `https://raw.githubusercontent.com/${REPO}/${BRANCH}/${entry.path}/SKILL.md`;
      return {
        ...entry,
        name,
        description,
        body: parsed.content.trim(),
        summary: extractSummary(parsed.content) || description,
        rawMdUrl,
        githubUrl: `https://github.com/${REPO}/tree/${BRANCH}/${entry.path}`,
        githubMdUrl: `https://github.com/${REPO}/blob/${BRANCH}/${entry.path}/SKILL.md`,
        installCommand: `scripts/install-skill-from-github.py \\\n+  --repo ${REPO} \\\n+  --path ${entry.path}`,
      };
    })
    .sort(sortSkills);
}

export function getSkill(id: string): Skill | undefined {
  return getSkills().find((skill) => skill.id === id);
}

export function getAllTags(skills = getSkills()): string[] {
  return Array.from(new Set(skills.flatMap((skill) => skill.tags ?? []))).sort((a, b) =>
    a.localeCompare(b),
  );
}
