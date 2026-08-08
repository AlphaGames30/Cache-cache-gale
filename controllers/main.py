from odoo import http, fields
from odoo.http import request

class CacheCacheController(http.Controller):

    # Route pour afficher l'interface de jeu
    @http.route('/game/<string:game_code>', type='http', auth='public', website=True)
    def game_page(self, game_code, **kw):
        game = request.env['cache.game'].sudo().search([('name', '=', game_code)], limit=1)
        if not game:
            return request.not_found()
            
        return request.render('cache_game.game_template', {
            'game': game
        })

    # Endpoint JSON appelé par le JavaScript du téléphone pour mettre à jour sa position
    @http.route('/game/update_location', type='json', auth='public', csrf=False)
    def update_location(self, player_id, latitude, longitude):
        player = request.env['cache.player'].sudo().browse(player_id)
        if not player.exists():
            return {'status': 'error', 'message': 'Joueur introuvable'}

        # 1. Mise à jour de la position dans la base de données
        player.write({
            'latitude': latitude,
            'longitude': longitude,
            'last_update': fields.Datetime.now()
        })

        # 2. Diffusion temps réel aux autres joueurs via le Bus Odoo
        channel_name = f"cache_game_{player.game_id.id}"
        payload = {
            'player_id': player.id,
            'player_name': player.name,
            'role': player.role,
            'latitude': latitude,
            'longitude': longitude,
        }
        
        # Envoie l'événement aux clients JavaScript abonnés
        request.env['bus.bus']._sendone(channel_name, 'gps_position_update', payload)

        return {'status': 'success'}
      
