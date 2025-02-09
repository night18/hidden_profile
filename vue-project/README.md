# vue-project

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

## Websocket Code Function Explanation

### Code (100)
- *Goal*: Add the participant to the group.
- *When*: After connecting to the web socket.
- *What*: Send the participant ID to the server.
- *Return*: {code: 100, group_members: array, startable: boolean}
