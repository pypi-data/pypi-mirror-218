from django import http
from django.http import FileResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.conf import settings

from .operations.explorer import ExplorerOperations
from .operations.location import LocationOperations
from .operations.action import ActionOperations
from .logger.logger import ExplorerLogger


class Explorer(TemplateView):
    template_name = 'explorer/index.html'
    http_method_names = ['get', 'post']
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.logger = ExplorerLogger()
        return None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return http.HttpResponseRedirect(f'{reverse("explorer-login")}?next={reverse("explorer-main")}')
        
        # GETTING RESPONSE
        response = super().dispatch(request, *args, **kwargs)
        
        # LOGGINF INFORMATION
        self.logger.log(request, response)
        return response
    
    def get(self, request, *args, **kwargs):
        # GETTING OPERATION OBJECT
        xo = ExplorerOperations(request)

        # PERFORMING VALIDATION
        if not xo.isValid():
            return self._render_warning(request, xo.getMessage())

        # GETTING VOLUME AND PATH INFORMATION
        volume_info, location_path = xo.getVolumeInfo(), xo.getLocationPath()
        if xo.getMessage():
            return self._render_warning(request, xo.getMessage())

        # GETTING LOCATION OBJECT
        lo = LocationOperations(volume_info, location_path)

        # IS LOCATION IS FILE
        if lo.isLocationFile():
            return self._render_file(request, lo.getLocationPath())

        # GETTING LOATION REATED DATA
        data_list = lo.getData() # Getting location file and dir data.
        summary_data = lo.getDataSummary() # Getting summary data.
        navigation_bar_data = lo.getNavigationBarData() # Getting navigation bar data.
        
        # GETTING ICONS INFORMATION
        data_list = self._addIconInformation(data_list)

        # GETTING EXPLORER RELATED DATA
        page_data = xo.getPageData(data_list) # Getting page data.
        pagination_data = xo.getPaginationData(page_data) # Getting pagination data.
        
        # MAKING CONTEXT 
        context = self.get_context_data()
        context.update({
            'volume_data': xo.getVolumeData(),
            'action_data': xo.getActionData(),
            'summary_data': summary_data,
            'navigation_bar_data': navigation_bar_data,
            'page_data': page_data,
            'pagination_data': pagination_data
        })
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # GETTING OPERATION OBJECT
        xo = ExplorerOperations(request)

        # PERFORMING VALIDATION
        if not xo.isValid():
            return self._render_warning(request, xo.getMessage())

        # GETTING VOLUME AND PATH INFORMATION
        volume_info, location_path = xo.getVolumeInfo(), xo.getLocationPath()
        if xo.getMessage():
            return self._render_warning(request, xo.getMessage())

        # GETTING LOCATION OBJECT
        lo = LocationOperations(volume_info, location_path)

        # GETTING LOCATION RELATED DATA
        data_list = lo.getData() # Getting location file and dir data.
        path_list = xo.getCheckedFilePath(data_list) # Getting page data.

        # PERFORMING ACTION
        ao = ActionOperations(volume_info, location_path)
        file_path = ao.performAction(xo.getAction(), path_list, xo.getFileData())
        if ao.getMessage():
            return self._render_warning(request, xo.getMessage())

        if file_path: # Download case
            return FileResponse(open(file_path, 'rb'), as_attachment=True)

        return self._redirect_to_same(request)

    def render_to_response(self, context, **response_kwargs) -> http.HttpResponse:
        
        return super().render_to_response(context, **response_kwargs)

    def _redirect_to_same(self, request):
        """Redirect to same url."""
        return http.HttpResponseRedirect(request.get_full_path())

    def _render_warning(self, request, message):
        """Rendered warning template"""
        return render(request, 'explorer/warning.html', {'message': message})
    
    def _render_error(self, request, message):
        """Rendered error template"""
        return render(request, 'explorer/error.html', {'message': message})

    def _render_file(self, request, file_path):
        """Return the file render response."""
        return FileResponse(open(file_path, 'rb'), as_attachment=False)
    
    def _addIconInformation(self, data_list):
        """Adding icon information if icon package is used."""
        # IF APP IS NOT USED
        if not ('vscode_icons' in settings.INSTALLED_APPS):
            return data_list
        
        # LOADING MODULE IF EXISTS
        try:
            from vscode_icons.vscode import VSCodeIcons
            vsi = VSCodeIcons()
        except:
            return data_list
        
        # UPDATING ICON INFORMATION
        icon_data = []
        for data in data_list:
            # GETTING TYPE AND NAME
            type = data['type']
            name = data['name']
            
            if type == 'directory':
                icon_path = vsi.findDirectoryIcon(name)
            else:
                icon_path = vsi.findFileIcon(name)
            data['icon'] = icon_path
            icon_data.append(data)
        return data_list