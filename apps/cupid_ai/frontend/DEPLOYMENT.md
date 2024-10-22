# Deployment with Squarespace

### Install netlify cli

- `npm install -g netlify-cli` -`netlify login`

### Deploy to netflify:

- `npm run build`
- `netlify deploy`

###

- You get a url, create an iframe in a squarespace page and insert the iframe as such:

```html
<iframe
  src="https://<your-netlify-url>.netlify.app"
  style="width: 100%; height: 100vh; border: none;"
></iframe>
```
