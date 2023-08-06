
          import {html} from "lit";
          export default html`<h1 id="user-test-configuration-menu-10-17-january-2022">User Test: Configuration menu (10-17 January, 2022)</h1>
<p>At the end of last year, we created one Configuration menu by merging Supervisor. In the next iteration, we want to organize our menu by creating logical grouping and combining duplicated features. We are conducting this test to see if we are on the right track.</p>
<ul>
<li>Anyone could join</li>
<li>Respondents recruited on Twitter, Reddit and Home Assistant Forum</li>
<li>This test is open for 10 days </li>
<li>UsabilityHub for user test</li>
<li>Figma for prototype</li>
<li>6 questions</li>
<li>3 tasks</li>
<li>Due to some limitations by UsabilityHub, it only worked on desktop</li>
</ul>
<h1 id="results">Results</h1>
<p>915 respondents took part in this test and they gave 407 comments. In general there isn’t a significant difference between:</p>
<ul>
<li>How long a respondent has been using Home Assistant</li>
<li>Installation method</li>
<li>How many visits to its Home Assistant in the past 3 months</li>
<li>Home Assistant expertise</li>
</ul>
<h2 id="overall-menu-change">Overall menu change</h2>
<p>This prototype organized our menu by creating logical grouping and combining duplicated features. What do people think of this change?</p>
<h3 id="stats">Stats</h3>
<ul>
<li>2% (21) Like extremely</li>
<li>30% (276) Like very much</li>
<li>53% (481) Neutral</li>
<li>12% (108) Dislike very much</li>
<li>3% (26) Dislike extremely</li>
</ul>
<p><em>3 respondents passed</em></p>
<h3 id="comments-summary">Comments summary</h3>
<p><strong>Like</strong></p>
<ul>
<li>Clean and decluttered</li>
<li>Style looks better</li>
<li>Faster to use</li>
<li>Merging Supervisor into different pages</li>
<li>Moving Developer tools to Settings</li>
</ul>
<p><strong>Dislike</strong></p>
<ul>
<li>Moving Developer tools to Settings</li>
<li>More clicks for scripts and helpers</li>
<li>Too many changes at once causes a high learning curve</li>
<li>Removing the word <code>Integrations</code> makes it harder to find them</li>
<li>Difference between <code>Addons</code> and <code>Services</code> is a bit subtle</li>
<li>No clear distinction between <code>Developer</code> and <code>System</code></li>
<li>Material Design got the Google image</li>
</ul>
<p><strong>Suggestions</strong></p>
<ul>
<li>More top level menu items for example logs.</li>
<li>What are settings and what not? Maybe better to name it <code>Configuration</code></li>
<li>Devices are a first-class citizen in the domain of Home Assistant, and so shouldn&#39;t be tucked away in &quot;Settings&quot;</li>
<li>Rename Developer tools (or make it only for Home Assistant developers)</li>
<li>Separate administration (for instance creating users / adding lights etc) from development activities (creating automations and scripts)</li>
<li>Search Bar in Settings</li>
<li>Feature to put menu items in sidebar</li>
<li>Unification of add-ons and integrations</li>
<li>Adding ‘New’ hints to show what changed</li>
<li>Give <code>About</code> a less prominent size</li>
<li>Accordion view option which puts every tab below</li>
<li>Dev mode and a Prod Mode</li>
<li>Always show config menu (on bigger screens)</li>
</ul>
<h3 id="conclusion">Conclusion</h3>
<p>We should keep our focus on organizing our menu by creating logical grouping and combining duplicated features. With these changes we make more people happy:</p>
<ul>
<li>Reconsider putting <code>Logs</code> as a top-level menu item</li>
<li>Add a search bar</li>
<li>Use the word <code>Integrations</code> with <code>Devices &amp; Services</code></li>
<li>Moving <code>Developer tools</code> to <code>Settings</code> is a good idea</li>
<li>Rename <code>Developer tools</code> to for example <code>Tools</code></li>
<li>Add <code>New</code> explanation popups to what has changed</li>
<li>We could rename <code>Configuration</code> to <code>Settings</code></li>
<li>Give <code>About</code> a less prominent size</li>
</ul>
<h2 id="helpers">Helpers</h2>
<p>In Home Assistant you can create toggles, text fields, number sliders, timers and counters. Also known as <code>Helpers</code>. Where should they be placed?</p>
<h3 id="stats-1">Stats</h3>
<ul>
<li>78% (709) respondents are using helpers. They use it for:</li>
<li>92% (645) automations and scenes</li>
<li>62% (422) dashboards</li>
<li>43% (296) virtual devices</li>
</ul>
<h3 id="comments-summary-1">Comments summary</h3>
<p>Some respondents commented that they think <code>Helpers</code> shouldn’t be listed under <code>Automations &amp; Services</code>. Although almost all respondents use it for that specific purpose.</p>
<h3 id="conclusion-1">Conclusion</h3>
<p>Helpers is, in addition to <code>Automations &amp; Services</code>, also partly seen as virtual devices and dashboard entities. </p>
<ul>
<li>We might consider promoting them in their own top-level menu item</li>
<li>Rename <code>Helpers</code> to something with <code>controls</code></li>
</ul>
<h2 id="add-person">Add person</h2>
<p>The first task in this user test was to add a person. Since this has not changed in the current menu structure, this should be an easy assignment. How do people experience the navigation to this feature?</p>
<h3 id="stats-2">Stats</h3>
<p>95% reached the goal screen and 98% marked the task as completed. There were 18 common paths.</p>
<p>After the task we asked how easy it was to add a person.</p>
<ul>
<li>41% (378) Extremely easy</li>
<li>48% (440) Fairly easy</li>
<li>7% (67) Neutral</li>
<li>2% (19) Somewhat difficult</li>
<li>1% (11) Very difficult</li>
</ul>
<h3 id="comments-summary-2">Comments summary</h3>
<p>*No mentionable comments *</p>
<h3 id="conclusion-2">Conclusion</h3>
<p>This test showed that the current navigation design works.</p>
<h2 id="yaml">YAML</h2>
<p>In Home Assistant you can make configuration changes in YAML files. To make these changes take effect you have to reload your YAML in the UI or do a restart. How are people doing this and can they find it in this new design?</p>
<h3 id="stats-3">Stats</h3>
<p>83% reached the goal screen and 87% marked the task as completed. There were 59 common paths.</p>
<p>After the task we asked how easy it was to reload the YAML changes.</p>
<ul>
<li>4% (40) Extremely easy</li>
<li>22% (204) Fairly easy</li>
<li>20% (179) Neutral</li>
<li>37% (336) Somewhat difficult</li>
<li>17% (156) Very difficult</li>
</ul>
<p>And we asked if they have seen that we&#39;ve moved some functionality from current <code>Server Controls</code> to <code>Developer Tools</code>.</p>
<ul>
<li>57% (517) Yes</li>
<li>43% (398) No</li>
</ul>
<h3 id="comments-summary-3">Comments summary</h3>
<p><strong>Like</strong></p>
<ul>
<li>YAML in Developer tools</li>
</ul>
<p><strong>Dislike</strong></p>
<ul>
<li>Hidden restart and reload</li>
<li>YAML in Developer Tools</li>
<li>Combining <code>Developer tools</code> with <code>Server management</code></li>
<li>Reload Home Assistant button isn&#39;t clear what it does</li>
<li>Reload/restart Home Assistant in Developer Tools</li>
</ul>
<p><strong>Suggestions</strong></p>
<ul>
<li>Reload all YAML button</li>
<li>Dev mode and a Prod Mode</li>
<li>Show restart/reload as buttons in System instead of overflow menu</li>
<li>Explain that you can reload YAML when you want to restart your system</li>
<li>YAML reloading under System</li>
</ul>
<h3 id="conclusion-3">Conclusion</h3>
<p>This test showed two different kinds of user groups: UI and YAML users. </p>
<ul>
<li>Moving <code>Developer tools</code> to <code>Settings</code> is a good idea</li>
<li>YAML users want reload YAML and Home Assistant restart in <code>System</code></li>
<li>Move the restart and reload button to the <code>System</code> page from the overflow menu</li>
<li>Add suggestion to reload YAML when a user wants to restart</li>
<li>Add reload all YAML button</li>
</ul>
<h2 id="logs">Logs</h2>
<h3 id="stats-4">Stats</h3>
<p>70% reached the goal screen and 77% marked the task as completed. There were 48 common paths.</p>
<p>After the task we asked to find out why your Elgato light isn&#39;t working.</p>
<ul>
<li>6% (57) Extremely easy</li>
<li>28% (254) Fairly easy</li>
<li>21% (188) Neutral</li>
<li>21% (196) Somewhat difficult</li>
<li>24% (220) Very difficult</li>
</ul>
<h3 id="comments-summary-4">Comments summary</h3>
<p><strong>Suggestions</strong></p>
<ul>
<li>Log errors on the integration page</li>
<li>Problem solving center</li>
</ul>
<h3 id="conclusion-4">Conclusion</h3>
<p>Although this test shows that a large number of respondents manage to complete the task, they find it difficult to find out the light isn’t working.</p>
<ul>
<li>Add logs errors/warnings to the integration page</li>
<li>Reconsider putting <code>Logs</code> as a top-level menu item</li>
</ul>
<h2 id="learnings-for-next-user-test">Learnings for next user test</h2>
<ul>
<li>Explain that topic is closed for comments so that you can do this test without any influence</li>
<li>Mobile test should work on mobile</li>
<li>Testing on an iPad got some bugs</li>
<li>People like doing these kind of test and we should do them more often</li>
</ul>
`
          