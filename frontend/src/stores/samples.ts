import{reactive}from 'vue';import{getBatches,getUnits,getTargets}from '../api/batches';import type{Batch,Unit,Target}from '../types/domain';
export const samples=reactive({batches:[]as Batch[],units:[]as Unit[],targets:[]as Target[]});
export async function loadBatches(){samples.batches=await getBatches();}
export async function loadUnits(id:number){samples.units=await getUnits(id);}
export async function loadTargets(id:number){samples.targets=await getTargets(id);}
