
          import {html} from "lit";
          export default html`<p><img src="/images/logo-with-text.png" alt="Home Assistant Logo"></p>
<h1 id="how-to-edit-designhome-assistantio">How to edit design.home-assistant.io</h1>
<p>All pages are stored in <a href="https://github.com/home-assistant/frontend/tree/dev/gallery/src/pages">the pages folder</a> on GitHub. Pages are grouped in a folder per sidebar section. Each page can contain a <code>&lt;page name&gt;.markdown</code> description file, a <code>&lt;page name&gt;.ts</code> demo file or both. If both are defined the description is rendered first. The description can contain metadata to specify the title of the page.</p>
<h2 id="development">Development</h2>
<p>You can develop design.home-assistant.io locally by checking out <a href="https://github.com/home-assistant/frontend">the Home Assistant frontend repository</a>. The command to run the gallery is <code>gallery/script/develop_gallery</code>. It will automatically open a browser window and load the development version of the website.</p>
<h2 id="creating-a-page">Creating a page</h2>
<p>Navigate to the <a href="https://github.com/home-assistant/frontend/tree/dev/gallery/src/pages">the pages folder</a> on GitHub. If the folder for your category does not exist yet, create it. Create a new Markdown file inside this folder for your description, ie <code>usability.markdown</code>. This filename will be used in the URL. Add the following content:</p>
<pre><code class="language-markdown">---
title: My new page
---

Hello and welcome to my new page!
</code></pre>
<p>Once saved, the page will be automatically added to the bottom of the sidebar. The title specified in the header will be shown as the page title and used in the sidebar.</p>
<h2 id="linking-the-page-in-the-sidebar">Linking the page in the sidebar</h2>
<p>By default the sidebar will gather all pages and group them by category. You can override the order of the categories, define a name for categories and change the order of the pages in <a href="https://github.com/home-assistant/frontend/blob/dev/gallery/sidebar.js"><code>sidebar.js</code></a>.</p>
<p>Any category not listed in <code>sidebar.js</code> will be placed at the end of the sidebar.</p>
<p>Any page not listed in <code>sidebar.js</code> will be placed at the end of its category.</p>
<h2 id="adding-a-demo-to-a-page">Adding a demo to a page</h2>
<p>Create a file next to the description file with the same name as the description file, but with the <code>.ts</code> extension: <code>usability.ts</code>. For this example, we assume that the category folder that contains <code>usability.markdown</code> and <code>usability.ts</code> is called <code>user-experience</code>. Add the following content to <code>usability.ts</code>:</p>
<pre><code class="language-ts">import { html, css, LitElement } from &quot;lit&quot;;
import { customElement } from &quot;lit/decorators&quot;;
import &quot;../../../../src/components/ha-card&quot;;

@customElement(&quot;demo-user-experience-usability&quot;)
export class DemoUserExperienceUsability extends LitElement {
  protected render() {
    return html\`
      &lt;ha-card&gt;
        &lt;div class=&quot;card-content&quot;&gt;Hello world!&lt;/div&gt;
      &lt;/ha-card&gt;
    \`;
  }

  static get styles() {
    return css\`
      ha-card {
        max-width: 600px;
        margin: 24px auto;
      }
    \`;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    &quot;demo-user-experience-usability&quot;: DemoUserExperienceUsability;
  }
}
</code></pre>
<p>Note that the demo deosn&#39;t need to render anything itself. It can also be used to declare web components to be used by the page description. Because page descriptions are using markdown, they can embed any HTML.</p>
<h2 id="publishing-changes">Publishing changes</h2>
<p>The website is automatically published whenever the source files in the <code>dev</code> branch change. So to get your changes published, open a pull request with your changes.</p>
`
          