using System.ComponentModel.DataAnnotations.Schema;

namespace pricemap.Infrastructure.Database.Model
{
    [Table("listings")]
    public class Listing
    {
        [Column("listing_id")]
        public int ListingId { get; set; }
        [Column("place_id")]
        public int PlaceId { get; set; }
        [Column("price")]
        public int Price { get; set; }
        [Column("area")]
        public int Area { get; set; }
        [Column("room_count")]
        public int RoomCount { get; set; }
    }
}
