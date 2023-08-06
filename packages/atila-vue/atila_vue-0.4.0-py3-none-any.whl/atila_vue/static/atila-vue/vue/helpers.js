$http = axios

// define prototype methods -----------------------------------
Number.prototype.format = function () {
  if(this==0) return "0"
  var reg = /(^[+-]?\d+)(\d{3})/
  var n = (this + '')
  while (reg.test(n)) n = n.replace (reg, '$1' + ',' + '$2')
    return n
}
String.prototype.format = function () {
  var num = parseFloat (this)
  if( isNaN(num) ) return "0"
  return num.format ()
}
String.prototype.titleCase = function () {
  return this.replace (/\w\S*/g, function (txt) {return txt.charAt(0).toUpperCase () + txt.substr (1).toLowerCase ();})
}
Date.prototype.unixepoch = function () {
  return Math.floor(this.getTime() / 1000)
}

Date.prototype.format = function(f) {
  if (!this.valueOf()) return " "
  var d = this;
  return f.replace(/(%Y|%y|%m|%d|%H|%I|%M|%S|%p|%a|%A|%b|%B|%w|%c|%x|%X|%k|%n|%D)/gi, function($1) {
    switch ($1) {
    case "%Y":
      return d.getFullYear()
    case "%y":
      return (d.getFullYear() % 1000).zfill(2)
    case "%m":
      return (d.getMonth() + 1).zfill(2)
    case "%d":
      return d.getDate().zfill(2);
    case "%H":
      return d.getHours().zfill(2)
    case "%I":
      return ((h = d.getHours() % 12) ? h : 12).zfill(2)
    case "%M":
      return d.getMinutes().zfill(2)
    case "%S":
      return d.getSeconds().zfill(2)
    case "%p":
      return d.getHours() < 12 ? "AM" : "PM"
    case "%w":
      return d.getDay()
    case "%c":
      return d.toLocaleString()
    case "%x":
      return d.toLocaleDateString()
    case "%X":
      return d.toLocaleTimeString()
    case "%b":
      return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][d.getMonth()]
    case "%B":
      return ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][d.getMonth()]
    case "%a":
      return ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][d.getDay()]
    case "%A":
      return ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][d.getDay()]
    case "%k":
      return ['일', '월', '화', '수', '목', '금', '토'][d.getDay()]
    case "%n":
      return ( d.getMonth() + 1)
    case "%D":
      return d.getDate()
    default:
      return $1
    }
  })
}
String.prototype.repeat = function(len){var s = '', i = 0; while (i++ < len) { s += this; } return s;}
String.prototype.zfill = function(len){return "0".repeat(len - this.length) + this}
Number.prototype.zfill = function(len){return this.toString().zfill(len)}
















const _deviceDetect = {
  android: function() {
    return navigator.userAgent.match(/Android/i)
  },
  ios: function() {
    return navigator.userAgent.match(/iPhone|iPad|iPod/i)
  },
  mobile: function() {
    return (deviceDetect.android() || deviceDetect.ios())
  },
  touchable: function () {
    return (navigator.maxTouchPoints || 'ontouchstart' in document.documentElement)
  },
  rotatable: function () {
    return window.orientation > -1
  },
  width: function () {
    return window.innerWidth
  },
  height: function () {
    return window.innerHeight
  }
}
device = _deviceDetect


















const swsync = {
  periodic_sync_enabled: async function () {
    const status = await navigator.permissions.query({
      name: 'periodic-background-sync',
    })
    return status.state === 'granted'
  },

  register_tag: async function (tag, min_interval_sec = 0) {
    if (!('serviceWorker' in navigator && 'SyncManager' in window)) return false
    const registration = await navigator.serviceWorker.ready
    if (min_interval_sec) {
      const enabled = await this.periodic_sync_enabled ()
      if (!enabled) return false
      await registration.periodicSync.register (tag, {minInterval: min_interval_sec * 1000})
    } else {
      await registration.sync.register (tag)
    }
    return true
  },

  unregister_tag: async function (tag) {
    if (!('serviceWorker' in navigator && 'SyncManager' in window)) return false
    const enabled = await this.periodic_sync_enabled ()
    if (!enabled) return
    const registration = await navigator.serviceWorker.ready
    await registration.periodicSync.unregister(tag)
  },

  is_tag_registered: async function (tag) {
    if (!('serviceWorker' in navigator && 'SyncManager' in window)) return false
    const enabled = await this.periodic_sync_enabled ()
    if (!enabled) return
    const registration = await navigator.serviceWorker.ready
    const tags = await registration.periodicSync.getTags()
    return tags.includes(tag)
  },
}




















axios.interceptors.request.use ( async (config) => {
  if (!("common" in config.headers)) {
    return config
  }
  const atk = config.headers.common.Authorization
  if (!atk) {
    return config
  }
  if (config.url == store.state.$refresh_token_api) {
    return config
  }
  if (config.url.substring (0, 1) != '/') {
    return config
  }
  let exp
  if (!!store.state.$claims) {
    exp = store.state.$claims.exp
  } else {
    exp = dejwt (atk.substring (7, atk.length)).exp
  }
  if (exp > new Date ().unixepoch () - 60) {
    const access_token = await backend.refresh_access_token ()
    if (!!access_token) {
      config.headers.common.Authorization = `Bearer ${ access_token }`
    }
  }
  return config
}, (error) => {
  return Promise.reject (error)
})

class AsynWebSocket extends WebSocket {
  constructor (url, read_handler = (evt) => log (evt.data)) {
    super (url)
    this.onmessage = read_handler
    this.buffer = []
    this.connected = false
  }

  onwrite() {
    for (var i = 0; i < this.buffer.length; i++) {
      msg = this.buffer.shift ()
      log (`send: ${ msg }`, 'websocket')
      this.sock.send (msg)
    }
  }

  onopen() {
    this.connected = true
    log ('connected', 'websocket')
    this.onwrite ()
  }

  onclose (evt) {
    this.connected = false
    log ('closed', 'websocket')
  }

  push(msg) {
    if (!msg) { return }
    this.buffer.push (msg)
    if (!this.connected) {
      return
    }
    this.onwrite ()
  }
}

function FailSafeWebSocket (buffer = []) {
  const ws = store.state.$websocket
  ws.sock = new AsynWebSocket (ws.url, ws.read_handler)
  ws.sock.buffer = buffer
  ws.push = ws.sock.push
  log ('connecting...', 'websocket')

  ws.sock.onerror = function (e) {
    log ('error occurred, try to reconnect...', 'websocket')
    const buffer = [...ws.sock.buffer]
    ws.sock.close ()
    FailSafeWebSocket (buffer)
  }
}

const backend = {
  // Authorization -----------------------------------
  refresh_access_token: async function (endpoint = null) {
    if (!!endpoint) { // initial set
      store.state.$refresh_token_api = endpoint
    }
    const _endpoint = store.state.$refresh_token_api
    if (!_endpoint) {
      log ('does not call refresh_access_token (API_ID)', 'warn')
      return
    }
    const access_token = store.state.$ls.get ('access_token')
    if (!access_token) {
      store.commit ('_clear_credential')
      return
    }

    let claim = dejwt (access_token)
    if (!claim) { // corrupted token
      store.commit ('_clear_credential')
      return
    }

    if (claim.exp > new Date ().unixepoch () + 120) { // over 2 minutes to expiration
      if (!API_ID) {
        return // this is called by axio hook, nothing to do, all is ok
      }
      store.commit ("_save_credential", {uid: claim.uid, grp: claim.grp, access_token})
      return access_token
    }

    const rtk = store.state.$ls.get ('refresh_token')
    if (!rtk) {
      store.commit ('_clear_credential')
      return
    }

    axios.defaults.headers.common ["Authorization"] = `Bearer ${access_token}`
    let r = null
    try {
      r = await axios.post (_endpoint, {refresh_token: rtk})
    } catch (e) {
      traceback (e)
      r = e.response
      if (r.status == 401) {
        store.commit ('_clear_credential')
      }
      return
    }
    claim = dejwt (r.data.access_token)
    store.commit ("_save_credential", {uid: claim.uid, grp: claim.grp, access_token: r.data.access_token, refresh_token: r.data.refresh_token})
    return r.data.access_token
  },

  signin_with_id_and_password: async function (endpoint, payload) {
    let r = null
    try {
        r = await axios.post (endpoint, payload)
    } catch (e) {
        r = e.response
        const msg = traceback (e)
        if (r.status == 401) {
          store.commit ('_clear_credential')
        }
        return msg
    }
    const claim = dejwt (r.data.access_token)
    store.commit ("_save_credential", {uid: claim.uid, grp: claim.grp, access_token: r.data.access_token, refresh_token: r.data.refresh_token})
  },

  create_websocket: function (endpoint, read_handler) {
    const ws = store.state.$websocket
    ws.url = endpoint
    ws.read_handler = read_handler
    FailSafeWebSocket ([])
    return ws
  },

  // URL Building -----------------------------------------
  _check_url: function (url) {
    if (url.substring (0, 1) == '/') {
      throw new Error ('url cannot be started with /')
    }
  },

  _urlfor: function (urlspecs, name, args = [], _kargs = {}) {
    const target = urlspecs [name]
    if (!target) {
      throw new Error (`route ${name} not found`)
    }

    let url = target.path

    let kargs = {}
    if (Object.prototype.toString.call(args).indexOf ("Array") != -1) {
      let i = 0
      for (let k of target.params) {
        kargs [k] = args [i]
        i += 1
      }
      for (let k of target.query) {
        kargs [k] = args [i]
        i += 1
      }
    } else {
      kargs = args
    }

    for (let k of target.params) {
      if (kargs [k] !== undefined ) {
        url = url.replace (":" + k, kargs [k])
      }
    }

    let newquery = ''
    for (let k of target.query) {
      if (kargs [k] === undefined ) {
        continue
      }
    const v = kargs [k]
    if (!!newquery) {
      newquery += '&'
    }
    newquery += k + "=" + encodeURIComponent (v)
    }

    if (!!newquery) {
      return url + "?" + newquery
    }
    return url
  },

  _route: function (name, args = [], _kargs = {}) {
    return this._urlfor (store.state.$urlspecs, name, args, _kargs)
  },

  endpoint: function (name, args = [], _kargs = {}) {
    if (name in store.state.$apispecs) {
      return this._urlfor (store.state.$apispecs, name, args, _kargs)
    }
    return this._route (name, args, _kargs)
  },

  static: function (relurl) {
    this._check_url (relurl)
    return store.state.$static_url + relurl
  },

  media: function (relurl) {
    this._check_url (relurl)
    return store.state.$media_url + relurl
  },
}



















// utilities ---------------------------------------------
function permission_granted  () {
  const next_route = store.state.$next_route || { name: 'index' }
  store.state.$next_route = null
  router.push (next_route)
}


function permission_required (permission, redirect, next) {
  if (store.state.$uid !== null) {
    if (store.state.$grp === null) {
      store.state.$grp = ['user']
    }

    if (store.state.$grp.indexOf ('admin') != -1) {
      return next ()
    }
    if (store.state.$grp.indexOf ('staff') != -1 && permission.indexOf ('staff') != -1) {
      return next ()
    }

    let granted = false
    for (const perm  of store.state.$grp) {
      if (permission.indexOf (perm) != 1) {
        granted = true
        break
      }
    }
    if (granted) {
      return next ()
    }
  }
  store.state.$next_route = {name: router.currentRoute.value.name}
  return next (redirect)
}



const _notificaton = {
  ask_permission: function (callback) {
    function handlePermission(permission) {
      if (!("permission" in Notification)) {
        Notification.permission = permission
      }
      if (callback) { callback () }
    }

    if (!("Notification" in window)) {
      return
    } else {
      if (this._check()) {
        Notification.requestPermission().then((permission) => {
          handlePermission(permission)
        })
      } else {
        Notification.requestPermission(function (permission) {
          handlePermission(permission)
        })
      }
    }
  },

  _check: function () {
    try {
      Notification.requestPermission().then();
    } catch (e) {
      return false;
    }
    return true;
  }
}

function push_alarm (title, message, link = null, icon = null, timeout = 10000) {
  if (Notification.permission === "denied") {
    log ("notification blocked")
    return
  }
  else if (Notification.permission !== "granted") {
    _notificaton.ask_permission (() => push_alarm (title, message, link, icon, timeout))
    return
  }
  const options = {body: message}
  if (!!icon) options.icon = icon
  const n = new Notification (title, options)
  n.onclick = (event) => {
    if (!!link) {
      window.open (link)
    }
    else n.close ()
  }
  n.onshow = (event) => {
    setTimeout(function(){ n.close () }, timeout)
  }
}


function log (msg, type = 'info') {
  if (store.state.$debug) {
    console.log (`[${type}] ${msg}`)
  }
}

function traceback (e) {
  let msg = ''
  if (e.response !== undefined) {
    const r = e.response
    let code = r.data.code || 70000
    let message = r.data.message || 'no message'
    msg = `${message} (status: ${r.status}, error: ${code})`
    log (msg + ' ' + JSON.stringify (r.data), 'expt')
  }
  else {
    msg = `${e.name}: ${e.message}`
    log (msg + ' ' + e, 'expt')
  }
  return msg
}

function dejwt (token) {
  try {
    return JSON.parse (atob (token.split ('.') [1]))
  } catch (e) {
    return null
  }
}

function load_script (src, callback = () => {}) {
  let current = null
  if (typeof (src) === "string") {
    current = src
    src = []
  } else {
    current = src.shift ()
  }
  var script = document.createElement('script')
  script.setAttribute('src', current)
  script.setAttribute('async', true)
  if (src.length) {
    script.addEventListener('load', () => { this.$load_script (src, callback) })
  } else {
    script.addEventListener('load', callback)
  }
  document.head.appendChild(script)
}

function set_cloak (flag) {
  store.state.$cloak = flag
}

function sleep (ms) {
  return new Promise (resolve => setTimeout(resolve, ms))
}

function build_url (baseurl, params = {}) {
  let url = baseurl
  let newquery = ''
  for (let [k, v] of Object.entries (params)) {
    if (v === null) {
      continue
    }
  if (!!newquery) {
    newquery += '&'
  }
  newquery += k + "=" + encodeURIComponent (v)
  }
  if (!!newquery) {
    return url + "?" + newquery
  }
  return url
}

async function keep_offset_bottom (css, margin = 0, initial_delay = 0) {
  function fixed (event) {
    const obj = document.querySelector (css)
    obj.style.height = (window.innerHeight - obj.offsetTop - margin) + 'px'
  }
  addEventListener("resize", (event) => {fixed (event)})
  await sleep (initial_delay)
  fixed ()
}

async function keep_offset_right (css, margin = 0, initial_delay = 0) {
  function fixed (event) {
    const obj = document.querySelector (css)
    obj.style.width = (window.innerWidth - obj.offsetLeft - margin) + 'px'
  }
  addEventListener("resize", (event) => {fixed (event)})
  await sleep (initial_delay)
  fixed ()
}
