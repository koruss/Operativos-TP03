import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MaterialModule } from './material/material.module';

import { AppComponent } from './app.component';
import { FileViewComponent } from './Components/file-view/file-view.component';
import { CreateDirectoryComponent } from './Components/create-directory/create-directory.component';
import { CreateFileComponent } from './Components/create-file/create-file.component';
import { UploadFileComponent } from './Components/upload-file/upload-file.component';
import { MoveComponent } from './Components/move/move.component';
import { SpaceAllocatorComponent } from './Components/space-allocator/space-allocator.component';
import { FileExplorerComponent } from './Components/file-explorer/file-explorer.component';
import { SearchComponent } from './Components/search/search.component';

@NgModule({
  declarations: [AppComponent,  FileViewComponent, CreateDirectoryComponent, CreateFileComponent, UploadFileComponent, MoveComponent, SpaceAllocatorComponent, FileExplorerComponent, SearchComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MaterialModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
