import js from "@eslint/js";

export default [
  js.configs.recommended,
  {
    rules: {
      "no-unused-vars": "warn",
      "no-undef": "warn",
      "max-lines": [
        "error",
        { max: 500, skipBlankLines: true, skipComments: true },
      ],
    },
    ignores: ["**/Extensions/"],
  },
];
