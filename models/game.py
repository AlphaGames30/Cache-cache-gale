from odoo import models, fields, api

class CacheGame(models.Model):
    _name = 'cache.game'
    _description = 'Session de Cache-Cache GPS'

    name = fields.Char(string="Code du salon", required=True, index=True)
    state = fields.Selection([
        ('draft', 'En attente'),
        ('in_progress', 'En cours'),
        ('done', 'Terminé')
    ], default='draft', string="État")
    
    player_ids = fields.One2many('cache.player', 'game_id', string="Joueurs")


class CachePlayer(models.Model):
    _name = 'cache.player'
    _description = 'Joueur dans une partie'

    name = fields.Char(string="Pseudo", required=True)
    game_id = fields.Many2one('cache.game', string="Partie", ondelete='cascade')
    
    role = fields.Selection([
        ('seeker', 'Chercheur'),
        ('hider', 'Caché')
    ], default='hider', required=True)
    
    latitude = fields.Float(string="Latitude", digits=(10, 7))
    longitude = fields.Float(string="Longitude", digits=(10, 7))
    last_update = fields.Datetime(string="Dernière mise à jour")
