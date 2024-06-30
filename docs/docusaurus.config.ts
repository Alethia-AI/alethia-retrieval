/** @type {import('@docusaurus/types').DocusaurusConfig} */
const math = require("remark-math");
const katex = require("rehype-katex");

module.exports = {
  title: "Privocia",
  tagline: "Privocia is the retrieval engine for LLMs.",
  url: "https://docs.privocia.re",
  baseUrl: "/",
  onBrokenLinks: "ignore",
  //deploymentBranch: 'master',
  onBrokenMarkdownLinks: "warn",
  favicon: "img/favicon.ico",
  organizationName: "privocia",
  trailingSlash: false,
  projectName: "privocia-org.github.io",
  themeConfig: {
    navbar: {
      //title: 'privocia',
      logo: {
        alt: "privocia",
        src: "img/privocia.png",
      },
      items: [
        {
          type: "doc",
          docId: "welcome",
          position: "left",
          label: "Docs",
        },

        { to: "blog", label: "Blog", position: "left" },
        {
          type: "doc",
          docId: "faq",
          position: "left",
          label: "FAQ",
        },
        {
          href: "https://app.privocia.re",
          position: "right",
          label: "Get API Key",
        },
        {
          href: "mailto:support@alehtia.re",
          position: "left",
          label: "Contact",
        },
        {
          href: "https://github.com/privocia-org/privocia-python",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "Community",
          items: [
            {
              label: "Discord",
              href: "https://discord.gg/8YkBcCED5y",
            },
            {
              label: "Twitter",
              href: "https://twitter.com/privocia",
            },
            {
              label: "LinkedIn",
              href: "https://www.linkedin.com/company/privocia/",
            },
          ],
        },
        {
          title: "Company",
          items: [
            {
              label: "Homepage",
              href: "https://privocia.re",
            },
            {
              label: "Contact",
              href: "mailto:support@privocia.re",
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Tavily.`,
    },
  },
  presets: [
    [
      "@docusaurus/preset-classic",
      {
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
          // Please change this to your repo.
          editUrl:
            "https://github.com/privocia-org/privocia-docs/tree/master/docs",
          remarkPlugins: [math],
          rehypePlugins: [katex],
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      },
    ],
  ],
  stylesheets: [
    {
      href: "https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.css",
      integrity:
        "sha384-Um5gpz1odJg5Z4HAmzPtgZKdTBHZdw8S29IecapCSB31ligYPhHQZMIlWLYQGVoc",
      crossorigin: "anonymous",
    },
  ],

  plugins: [
    // ... Your other plugins.
    [
      require.resolve("@easyops-cn/docusaurus-search-local"),
      {
        // ... Your options.
        // `hashed` is recommended as long-term-cache of index file is possible.
        hashed: true,
        blogDir: "./blog/",
        // For Docs using Chinese, The `language` is recommended to set to:
        // ```
        // language: ["en", "zh"],
        // ```
        // When applying `zh` in language, please install `nodejieba` in your project.
      },
    ],
  ],
};
