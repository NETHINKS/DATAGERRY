/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 NETHINKS GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CollectionTemplateListComponent } from './collection-template-list/collection-template-list.component';
import { CollectionListComponent } from './collection-list/collection-list.component';
import { CollectionAddComponent } from './collection-add/collection-add.component';

const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    component: CollectionListComponent,
    data: {
      breadcrumb: 'List'
    }
  },
  {
    path: 'add',
    component: CollectionAddComponent,
    data: {
      breadcrumb: 'Add'
    }
  },
  {
    path: 'template',
    pathMatch: 'full',
    component: CollectionTemplateListComponent,
    data: {
      breadcrumb: 'Template'
    }
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CollectionRoutingModule {
}