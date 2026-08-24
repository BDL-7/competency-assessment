window.DECK_CONTENT = {
  meta: {
    shortTitle: "Presentation Example",
    title: "Public-safe presentation example",
    presenter: "Project team",
    organization: "",
    date: "",
    visualStyle: { fontFamily: "system-sans", fontScale: "standard", colorScheme: "midnight" }
  },
  slides: [
    {
      id: "example-cover",
      layout: "title",
      section: "Example",
      title: "Public-safe presentation example",
      highlight: "presentation",
      subtitle: "Replace synthetic content only with material approved for its destination.",
      bullets: [
        { color: "cyan", html: "<strong>Source:</strong> approved project inputs" },
        { color: "green", html: "<strong>Data:</strong> synthetic or release-approved" }
      ],
      credits: "Reusable HTML workshop"
    },
    {
      id: "example-controls",
      layout: "cards",
      section: "Example",
      title: "Repository publishing controls",
      highlight: "controls",
      subtitle: "Keep implementation source separate from controlled inputs and generated output.",
      columns: 3,
      cards: [
        { accent: "cyan", title: "Commit", body: "Source, tests, schemas, setup instructions, and synthetic fixtures." },
        { accent: "purple", title: "Control", body: "Operational data, governed documents, and presenter notes." },
        { accent: "green", title: "Generate", body: "Portable HTML, PDFs, renders, reports, and release packages." }
      ]
    }
  ]
};
