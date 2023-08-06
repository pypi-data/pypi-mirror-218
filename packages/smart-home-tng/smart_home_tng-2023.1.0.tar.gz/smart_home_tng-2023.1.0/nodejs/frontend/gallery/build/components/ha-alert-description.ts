
          import {html} from "lit";
          export default html`<h1 id="alert-ha-alert">Alert <code>&lt;ha-alert&gt;</code></h1>
<p>The alert offers four severity levels that set a distinctive icon and color.</p>
<ha-alert alert-type="error">
  This is an error alert — check it out!
</ha-alert>

<ha-alert alert-type="warning">
  This is an warning alert — check it out!
</ha-alert>

<ha-alert alert-type="info">
  This is an info alert — check it out!
</ha-alert>

<ha-alert alert-type="success">
  This is an success alert — check it out!
</ha-alert>

<p><strong>Note:</strong> This component is by <a href="https://mui.com/components/alert/" rel="noopener noreferrer" target="_blank">MUI</a> and is not documented in the <a href="https://material.io" rel="noopener noreferrer" target="_blank">Material Design guidelines</a>.</p>
<ol>
<li><a href="#guidelines">Guidelines</a></li>
<li><a href="#implementation">Implementation</a></li>
</ol>
<h3 id="resources">Resources</h3>
<table>
<thead>
<tr>
<th>Type</th>
<th>Link</th>
<th>Status</th>
</tr>
</thead>
<tbody><tr>
<td>Design</td>
<td><a href="https://www.figma.com/community/file/967153512097289521/Home-Assistant-DesignKit" rel="noopener noreferrer" target="_blank">Home Assistant DesignKit</a> (Figma)</td>
<td>Available</td>
</tr>
<tr>
<td>Implementation</td>
<td><a href="https://github.com/home-assistant/frontend/blob/dev/src/components/ha-alert.ts" rel="noopener noreferrer" target="_blank">Web Component</a> (GitHub)</td>
<td>Available</td>
</tr>
</tbody></table>
<h2 id="guidelines">Guidelines</h2>
<h3 id="usage">Usage</h3>
<p>An alert displays a short, important message in a way that attracts the user&#39;s attention without interrupting the user&#39;s task.</p>
<h3 id="anatomy">Anatomy</h3>
<p><em>Documentation coming soon</em></p>
<h3 id="error-alert">Error alert</h3>
<p>Error alerts
<em>Real world example coming soon</em></p>
<h3 id="warning-alert">Warning alert</h3>
<p>Warning alerts
<em>Real world example coming soon</em></p>
<h3 id="info-alert">Info alert</h3>
<p>Info alerts
<em>Real world example coming soon</em></p>
<h3 id="success-alert">Success alert</h3>
<p>Success alerts
<em>Real world example coming soon</em></p>
<h3 id="placement">Placement</h3>
<h3 id="accessibility">Accessibility</h3>
<p>(WAI-ARIA: <a href="https://www.w3.org/TR/wai-aria-practices/#alert">https://www.w3.org/TR/wai-aria-practices/#alert</a>)</p>
<p>When the component is dynamically displayed, the content is automatically announced by most screen readers. At this time, screen readers do not inform users of alerts that are present when the page loads.</p>
<p>Using color to add meaning only provides a visual indication, which will not be conveyed to users of assistive technologies such as screen readers. Ensure that information denoted by the color is either obvious from the content itself (for example the visible text), or is included through alternative means, such as additional hidden text.</p>
<p>Actions must have a tab index of 0 so that they can be reached by keyboard-only users.</p>
<h2 id="implementation">Implementation</h2>
<h3 id="example-usage">Example Usage</h3>
<p><strong>Alert type</strong></p>
<ha-alert alert-type="error">
  This is an error alert — check it out!
</ha-alert>

<ha-alert alert-type="warning">
  This is an warning alert — check it out!
</ha-alert>

<ha-alert alert-type="info">
  This is an info alert — check it out!
</ha-alert>

<ha-alert alert-type="success">
  This is an success alert — check it out!
</ha-alert>


<pre><code class="language-html">&lt;ha-alert alert-type=&quot;error&quot;&gt;
  This is an error alert — check it out!
&lt;/ha-alert&gt;
&lt;ha-alert alert-type=&quot;warning&quot;&gt;
  This is a warning alert — check it out!
&lt;/ha-alert&gt;
&lt;ha-alert alert-type=&quot;info&quot;&gt;
  This is an info alert — check it out!
&lt;/ha-alert&gt;
&lt;ha-alert alert-type=&quot;success&quot;&gt;
  This is a success alert — check it out!
&lt;/ha-alert&gt;
</code></pre>
<p><strong>Title</strong></p>
<p>The <code>title </code> option should not be used without a description.</p>
<ha-alert alert-type="success" title="Success">
  This is an success alert — check it out!
</ha-alert>

<pre><code class="language-html">&lt;ha-alert alert-type=&quot;success&quot; title=&quot;Success&quot;&gt;
  This is an success alert — check it out!
&lt;/ha-alert&gt;
</code></pre>
<p><strong>Dismissable</strong></p>
<ha-alert alert-type="success" dismissable>
  This is an success alert — check it out!
</ha-alert>

<pre><code class="language-html">&lt;ha-alert alert-type=&quot;success&quot; dismissable&gt;
  This is an success alert — check it out!
&lt;/ha-alert&gt;
</code></pre>
<p><strong>Slotted action</strong></p>
<ha-alert alert-type="success">
  This is an success alert — check it out!
  <mwc-button slot="action" label="Undo"></mwc-button>
</ha-alert>

<pre><code class="language-html">&lt;ha-alert alert-type=&quot;success&quot;&gt;
  This is an success alert — check it out!
  &lt;mwc-button slot=&quot;action&quot; label=&quot;Undo&quot;&gt;&lt;/mwc-button&gt;
&lt;/ha-alert&gt;
</code></pre>
<p><strong>Slotted icon</strong></p>
<p><em>Documentation coming soon</em></p>
<p><strong>Right to left</strong></p>
<ha-alert alert-type="success" rtl>
  This is an info alert — check it out!
</ha-alert>

<pre><code class="language-html">&lt;ha-alert alert-type=&quot;success&quot; rtl&gt;
  This is an info alert — check it out!
&lt;/ha-alert&gt;
</code></pre>
<h3 id="api">API</h3>
<p><strong>Properties/Attributes</strong></p>
<table>
<thead>
<tr>
<th>Name</th>
<th>Type</th>
<th>Default</th>
<th>Description</th>
</tr>
</thead>
<tbody><tr>
<td>title</td>
<td>string</td>
<td>\`\`</td>
<td>Title to display.</td>
</tr>
<tr>
<td>alertType</td>
<td>string</td>
<td><code>info</code></td>
<td>Severity level that set a distinctive icon and color.</td>
</tr>
<tr>
<td>dismissable</td>
<td>boolean</td>
<td><code>false</code></td>
<td>Gives the option to close the alert.</td>
</tr>
<tr>
<td>icon</td>
<td>string</td>
<td>\`\`</td>
<td>Icon to display.</td>
</tr>
<tr>
<td>action</td>
<td>string</td>
<td>\`\`</td>
<td>Add an action button to the alert.</td>
</tr>
<tr>
<td>rtl</td>
<td>boolean</td>
<td><code>false</code></td>
<td>Support languages that use right-to-left.</td>
</tr>
</tbody></table>
<p><strong>Events</strong></p>
<p><em>Documentation coming soon</em></p>
<p><strong>CSS Custom Properties</strong></p>
<p><em>Documentation coming soon</em></p>
`
          