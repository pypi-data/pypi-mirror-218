export const PAGES = {
  "automation/describe-action": {
      metadata: {"title":"Describe Action"},
      
      demo: () => import("../src/pages/automation/describe-action")

    },
  "automation/describe-condition": {
      metadata: {"title":"Describe Condition"},
      
      demo: () => import("../src/pages/automation/describe-condition")

    },
  "automation/describe-trigger": {
      metadata: {"title":"Describe Trigger"},
      
      demo: () => import("../src/pages/automation/describe-trigger")

    },
  "automation/editor-action": {
      metadata: {"title":"Actions"},
      
      demo: () => import("../src/pages/automation/editor-action")

    },
  "automation/editor-condition": {
      metadata: {"title":"Conditions"},
      
      demo: () => import("../src/pages/automation/editor-condition")

    },
  "automation/editor-trigger": {
      metadata: {"title":"Triggers"},
      
      demo: () => import("../src/pages/automation/editor-trigger")

    },
  "automation/trace-timeline": {
      metadata: {"title":"Trace Timelines"},
      
      demo: () => import("../src/pages/automation/trace-timeline")

    },
  "automation/trace": {
      metadata: {"title":"Trace Graphs"},
      
      demo: () => import("../src/pages/automation/trace")

    },
  "brand/logo": {
      metadata: {"title":"Logo"},
      description: () => import("./brand/logo-description").then(m => m.default),
      

    },
  "brand/our-story": {
      metadata: {"title":"Our story"},
      description: () => import("./brand/our-story-description").then(m => m.default),
      

    },
  "components/ha-alert": {
      metadata: {"title":"Alerts","subtitle":"An alert displays a short, important message in a way that attracts the user's attention without interrupting the user's task."},
      description: () => import("./components/ha-alert-description").then(m => m.default),
      demo: () => import("../src/pages/components/ha-alert")

    },
  "components/ha-bar": {
      metadata: {"title":"Progress Bars"},
      
      demo: () => import("../src/pages/components/ha-bar")

    },
  "components/ha-chips": {
      metadata: {"title":"Chips"},
      
      demo: () => import("../src/pages/components/ha-chips")

    },
  "components/ha-faded": {
      metadata: {"title":"Faded Content"},
      
      demo: () => import("../src/pages/components/ha-faded")

    },
  "components/ha-form": {
      metadata: {"title":"Forms"},
      
      demo: () => import("../src/pages/components/ha-form")

    },
  "components/ha-label-badge": {
      metadata: {"title":"Label Badge"},
      
      demo: () => import("../src/pages/components/ha-label-badge")

    },
  "components/ha-selector": {
      metadata: {"title":"Selectors"},
      description: () => import("./components/ha-selector-description").then(m => m.default),
      demo: () => import("../src/pages/components/ha-selector")

    },
  "components/ha-tip": {
      metadata: {"title":"Tips"},
      
      demo: () => import("../src/pages/components/ha-tip")

    },
  "concepts/home": {
      metadata: {"title":"Home"},
      description: () => import("./concepts/home-description").then(m => m.default),
      

    },
  "design.home-assistant.io/editing": {
      metadata: {"title":"Editing design.home-assistant.io"},
      description: () => import("./design.home-assistant.io/editing-description").then(m => m.default),
      

    },
  "lovelace/alarm-panel-card": {
      metadata: {"title":"Alarm Panel Card"},
      
      demo: () => import("../src/pages/lovelace/alarm-panel-card")

    },
  "lovelace/area-card": {
      metadata: {"title":"Area Card"},
      
      demo: () => import("../src/pages/lovelace/area-card")

    },
  "lovelace/conditional-card": {
      metadata: {"title":"Conditional Card"},
      
      demo: () => import("../src/pages/lovelace/conditional-card")

    },
  "lovelace/entities-card": {
      metadata: {"title":"Entities Card"},
      
      demo: () => import("../src/pages/lovelace/entities-card")

    },
  "lovelace/entity-button-card": {
      metadata: {"title":"Entity Button Card"},
      
      demo: () => import("../src/pages/lovelace/entity-button-card")

    },
  "lovelace/entity-filter-card": {
      metadata: {"title":"Entity Filter Card"},
      
      demo: () => import("../src/pages/lovelace/entity-filter-card")

    },
  "lovelace/gauge-card": {
      metadata: {"title":"Gauge Card"},
      
      demo: () => import("../src/pages/lovelace/gauge-card")

    },
  "lovelace/glance-card": {
      metadata: {"title":"Glance Card"},
      
      demo: () => import("../src/pages/lovelace/glance-card")

    },
  "lovelace/grid-and-stack-card": {
      metadata: {"title":"Grid And Stack Card"},
      
      demo: () => import("../src/pages/lovelace/grid-and-stack-card")

    },
  "lovelace/iframe-card": {
      metadata: {"title":"Website Card"},
      
      demo: () => import("../src/pages/lovelace/iframe-card")

    },
  "lovelace/introduction": {
      metadata: {"title":"Introduction"},
      description: () => import("./lovelace/introduction-description").then(m => m.default),
      

    },
  "lovelace/light-card": {
      metadata: {"title":"Light Card"},
      
      demo: () => import("../src/pages/lovelace/light-card")

    },
  "lovelace/map-card": {
      metadata: {"title":"Map Card"},
      
      demo: () => import("../src/pages/lovelace/map-card")

    },
  "lovelace/markdown-card": {
      metadata: {"title":"Markdown Card"},
      
      demo: () => import("../src/pages/lovelace/markdown-card")

    },
  "lovelace/media-control-card": {
      metadata: {"title":"Media Control Card"},
      
      demo: () => import("../src/pages/lovelace/media-control-card")

    },
  "lovelace/media-player-row": {
      metadata: {"title":"Media Player Row"},
      
      demo: () => import("../src/pages/lovelace/media-player-row")

    },
  "lovelace/picture-elements-card": {
      metadata: {"title":"Picture Elements Card"},
      
      demo: () => import("../src/pages/lovelace/picture-elements-card")

    },
  "lovelace/picture-entity-card": {
      metadata: {"title":"Picture Entity Card"},
      
      demo: () => import("../src/pages/lovelace/picture-entity-card")

    },
  "lovelace/picture-glance-card": {
      metadata: {"title":"Picture Glance Card"},
      
      demo: () => import("../src/pages/lovelace/picture-glance-card")

    },
  "lovelace/plant-card": {
      metadata: {"title":"Plant Card"},
      
      demo: () => import("../src/pages/lovelace/plant-card")

    },
  "lovelace/shopping-list-card": {
      metadata: {"title":"Shopping List Card"},
      
      demo: () => import("../src/pages/lovelace/shopping-list-card")

    },
  "lovelace/thermostat-card": {
      metadata: {"title":"Thermostat Card"},
      
      demo: () => import("../src/pages/lovelace/thermostat-card")

    },
  "misc/integration-card": {
      metadata: {"title":"Integration Card"},
      
      demo: () => import("../src/pages/misc/integration-card")

    },
  "misc/util-long-press": {
      metadata: {"title":"Long Press Utility"},
      
      demo: () => import("../src/pages/misc/util-long-press")

    },
  "more-info/cover": {
      metadata: {"title":"Cover"},
      
      demo: () => import("../src/pages/more-info/cover")

    },
  "more-info/light": {
      metadata: {"title":"Light"},
      
      demo: () => import("../src/pages/more-info/light")

    },
  "more-info/update": {
      metadata: {"title":"Update"},
      
      demo: () => import("../src/pages/more-info/update")

    },
  "user-test/configuration-menu": {
      metadata: {"title":"User Test: Configuration menu"},
      description: () => import("./user-test/configuration-menu-description").then(m => m.default),
      

    },
  "user-test/user-types": {
      metadata: {"title":"User types"},
      description: () => import("./user-test/user-types-description").then(m => m.default),
      

    },
};
export const SIDEBAR = [
  {
    "category": "concepts",
    "pages": [
      "home"
    ]
  },
  {
    "category": "lovelace",
    "header": "Dashboards",
    "pages": [
      "introduction",
      "alarm-panel-card",
      "area-card",
      "conditional-card",
      "entities-card",
      "entity-button-card",
      "entity-filter-card",
      "gauge-card",
      "glance-card",
      "grid-and-stack-card",
      "iframe-card",
      "light-card",
      "map-card",
      "markdown-card",
      "media-control-card",
      "media-player-row",
      "picture-elements-card",
      "picture-entity-card",
      "picture-glance-card",
      "plant-card",
      "shopping-list-card",
      "thermostat-card"
    ]
  },
  {
    "category": "automation",
    "header": "Automation",
    "pages": [
      "editor-trigger",
      "editor-condition",
      "editor-action",
      "trace",
      "trace-timeline",
      "describe-action",
      "describe-condition",
      "describe-trigger"
    ]
  },
  {
    "category": "components",
    "header": "Components",
    "pages": [
      "ha-alert",
      "ha-bar",
      "ha-chips",
      "ha-faded",
      "ha-form",
      "ha-label-badge",
      "ha-selector",
      "ha-tip"
    ]
  },
  {
    "category": "more-info",
    "header": "More Info dialogs",
    "pages": [
      "cover",
      "light",
      "update"
    ]
  },
  {
    "category": "misc",
    "header": "Miscellaneous",
    "pages": [
      "integration-card",
      "util-long-press"
    ]
  },
  {
    "category": "brand",
    "header": "Brand",
    "pages": [
      "logo",
      "our-story"
    ]
  },
  {
    "category": "user-test",
    "header": "Users",
    "pages": [
      "user-types",
      "configuration-menu"
    ]
  },
  {
    "category": "design.home-assistant.io",
    "header": "About",
    "pages": [
      "editing"
    ]
  }
];
