import { writable } from 'svelte/store';
import { browser } from "$app/env";

export const team = writable(browser && localStorage.getItem("team") || "red")
team.subscribe((val) => browser && localStorage.setItem("team", val));


export const username = writable(browser && localStorage.getItem("username") || "player")
username.subscribe((val) => browser && localStorage.setItem("username", val));



export const state = writable({});
