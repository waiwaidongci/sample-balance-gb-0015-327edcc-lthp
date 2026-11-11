import{request,download}from './client';import type{Run}from '../types/domain';
export const getRuns=()=>request<Run[]>('/runs');export const getRun=(id:number)=>request<Run>(`/runs/${id}`);
export const createRun=(data:unknown)=>request<Run>('/runs',{method:'POST',body:JSON.stringify(data)});
export const retryRun=(id:number)=>request<Run>(`/runs/${id}/retry`,{method:'POST'});
export const exportRun=(id:number)=>download(`/runs/${id}/export`,`yy-weights-${id}.csv`);
