import { writable, readable } from 'svelte/store';
import { browser } from "$app/env";
import { io } from "socket.io-client";

export const team = writable(browser && localStorage.getItem("team") || "testing")
team.subscribe((val) => browser && localStorage.setItem("team", val));


export const username = writable(browser && localStorage.getItem("username") || "player")
username.subscribe((val) => browser && localStorage.setItem("username", val));

// export const state = writable(browser && localStorage.getItem("state") || {} )
// state.subscribe((val) => browser && localStorage.setItem("state", val));

export const state = writable({});

    