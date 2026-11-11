import{request}from './client';import type{Batch,Unit,Target}from '../types/domain';
export const getBatches=()=>request<Batch[]>('/batches');
export const createBatch=(data:unknown)=>request<Batch>('/batches',{method:'POST',body:JSON.stringify(data)});
export const getUnits=(id:number)=>request<Unit[]>(`/batches/${id}/units`);
export const importUnits=(id:number,csv_text:string)=>request<{imported:number}>(`/batches/${id}/import`,{method:'POST',body:JSON.stringify({csv_text})});
export const getTargets=(id:number)=>request<Target[]>(`/batches/${id}/targets`);
export const saveTargets=(id:number,targets:Target[])=>request<Target[]>(`/batches/${id}/targets`,{method:'PUT',body:JSON.stringify({targets})});
