import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { lastValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DirectoryService {
  constructor(private httpClient: HttpClient) {}

  /**
   * Retrieves from server directories data
   * @param path To the dir
   * @returns The response from the API
   */
  public getDir(path: string): Promise<any> {
    return lastValueFrom(this.httpClient.get('/api/dirs?dirPath=' + path));
  }

  /**
   * Creates a new directory
   * @param dirName The name of the directory
   * @param newDirPath The path of the new directory
   * @param forceOverwrite If directory should be overwritten
   * @returns If directory is created or not
   */
  public createDirectory(
    dirName: string,
    newDirPath: string,
    forceOverwrite: boolean
  ): Promise<any> {
    return lastValueFrom(
      this.httpClient.post('/api/dirs', { dirName, newDirPath, forceOverwrite })
    );
  }

  deleteDir(dir: { dirPath: string; dirName: any; }) {
    return lastValueFrom(this.httpClient.delete('/api/dirs',{"body":dir,"headers":{"Content-Type":"application/json"}}));
  }

  public shareDir(dir: any): Promise<any> {
    return lastValueFrom(this.httpClient.post('/api/dirs/share', dir));
  }

  public moveDir(dir: any): Promise<any> {
    return lastValueFrom(this.httpClient.post('/api/dirs/move', dir));
  }

  public copyDir(dir: any): Promise<any> {
    return lastValueFrom(this.httpClient.post('/api/dirs/vvcopy', dir));
  }
}
