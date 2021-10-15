import { writable, readable } from 'svelte/store';
import { browser } from "$app/env";
import { io } from "socket.io-client";

export const team = writable(browser && localStorage.getItem("team") || "testing")
team.subscribe((val) => browser && localStorage.setItem("team", val));


export const username = writable(browser && localStorage.getItem("username") || "player")
username.subscribe((val) => browser && localStorage.setItem("username", val));

export const state = writable({});

export const guesses = writable(0)

// export const guesses = writable();
    