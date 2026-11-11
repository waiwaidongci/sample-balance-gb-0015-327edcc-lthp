import{reactive}from 'vue';import{getRuns,getRun}from '../api/runs';import type{Run}from '../types/domain';
export const runs=reactive({items:[]as Run[],selected:null as Run|null});
export async function loadRuns(){runs.items=await getRuns();}
export async function loadRun(id:number){runs.selected=await getRun(id);}
