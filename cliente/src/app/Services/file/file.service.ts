import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { lastValueFrom } from 'rxjs';

import File from '../../Models/file.model';

@Injectable({
  providedIn: 'root',
})
export class FileService {
  constructor(private httpClient: HttpClient) {}

  /**
   * Creates a new file
   * @param fileData The data of the new file
   * @returns The information of the new file
   */
  public createFile(fileData: {
    filePath: string;
    extension: string;
    newFileName: string;
    content: string;
    forceOverwrite: boolean;
  }): Promise<any> {
    return lastValueFrom(this.httpClient.post<any>('/api/file', fileData));
  }

  public getFile(path: string, fileName: string): Promise<any> {
    return lastValueFrom(
      this.httpClient.get(
        '/api/file?filePath=' +
          path +
          '&fileName=' +
          fileName +
          '&contentOnly=false'
      )
    );
  }

  public modifyFile(file: any): Promise<any> {
    return lastValueFrom(this.httpClient.post('/api/file/modify', file));
  }

  public deleteFile(file: any): Promise<any> {
    return lastValueFrom(
      this.httpClient.delete('/api/file', {
        body: file,
        headers: { 'Content-Type': 'application/json' },
      })
    );
  }

  public moveFile(file: any): Promise<any> {
    return lastValueFrom(this.httpClient.post('/api/file/move', file));
  }

  public copyFile(file: any): Promise<any> {
    return lastValueFrom(this.httpClient.post('/api/file/vvcopy', file));
  }

  public shareFile(file: any): Promise<any> {
    return lastValueFrom(this.httpClient.post('/api/files/share', file));
  }
}
