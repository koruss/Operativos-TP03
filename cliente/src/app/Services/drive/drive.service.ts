import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { lastValueFrom } from 'rxjs';

import Drive from '../../Models/drive.model';

@Injectable({
  providedIn: 'root',
})
export class DriveService {
  private currentPath: string[] = [];

  constructor(private httpClient: HttpClient) {}

  /**
   * Retrieves from server directories data
   * @param dirData The retrieved info
   * @returns The response from the API
   */
  public getDriveSpace(username: string): Promise<any> {
    return lastValueFrom(
      this.httpClient.get('/api/drives/spaces?username=' + username)
    );
  }

  public getUsers(): Promise<any> {
    return lastValueFrom(
      this.httpClient.get('/api/drives')
    );
  }

  public getCurrentPath(): string[] {
    return this.currentPath;
  }

  public appendDirectoryToPath(directoryName: string): void {
    this.currentPath.push(directoryName);
  }

  public setCurrentPath(newPath: string[]): void {
    this.currentPath = newPath;
  }
}
