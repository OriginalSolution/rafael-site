# Adding a testimonial

Testimonials live in `testimonials.json`. Only add real stories, shared with the person's permission.
Add one object per story:

```json
[
  {
    "quote": "Their words, exactly as they agreed to share them.",
    "name": "Kwame A.",
    "detail": "30-day commitment",
    "anonymous": false
  }
]
```

- `quote` (required): the story text.
- `name` (optional): leave it out or set `"anonymous": true` to show "Anonymous".
- `detail` (optional): a short line such as the commitment length or city.

While the list is empty, the site shows a "Be one of the first stories" card instead.
