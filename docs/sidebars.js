/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

module.exports = {
  docsSidebar: [
    "welcome",
    {
      type: "category",
      label: "Privocia API",
      collapsible: true,
      collapsed: false,
      items: [
        "privocia-api/introduction",
        "privocia-api/python",
        "privocia-api/rest",
      ],
    },
    "contribution",
  ],
  // pydoc-markdown auto-generated markdowns from docstrings
  referenceSideBar: [require("./docs/reference/sidebar.json")],
};
