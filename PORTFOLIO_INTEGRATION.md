# Portfolio link

Add or verify in `my-website/src/lib/projects.ts`:

```ts
{
  id: 'guess-the-number',
  title: 'Guess the Number',
  // ...
  demoUrl: process.env.NEXT_PUBLIC_GUESS_THE_NUMBER_DEMO_URL ?? 'http://localhost:3010',
  github: 'https://github.com/emmarthur/guess-the-number',
}
```
